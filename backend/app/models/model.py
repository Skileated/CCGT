"""
Graph Transformer model for coherence scoring.

Implements graph attention network (GAT) with transformer-style aggregation.
Maps to SRS: Model Architecture and Scoring Requirements.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GATConv, global_mean_pool, global_max_pool
from torch_geometric.data import Data
from typing import Tuple
import logging

from ..core.config import settings, get_device

logger = logging.getLogger(__name__)


class GraphTransformer(nn.Module):
    """
    Graph Transformer model for coherence scoring.
    
    Architecture:
    - GAT layers for message passing
    - Multi-head attention aggregation
    - Scoring head with learned attention
    """
    
    def __init__(
        self,
        input_dim: int,
        hidden_dim: int = None,
        num_layers: int = None,
        num_heads: int = None,
        dropout: float = None
    ):
        super().__init__()
        
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim or settings.GNN_HIDDEN_DIM
        self.num_layers = num_layers or settings.GNN_NUM_LAYERS
        self.num_heads = num_heads or settings.GNN_NUM_HEADS
        self.dropout = dropout or settings.GNN_DROPOUT
        
        # Input projection
        self.input_proj = nn.Linear(input_dim, self.hidden_dim)
        
        # GAT layers
        self.gat_layers = nn.ModuleList()
        for i in range(self.num_layers):
            in_channels = self.hidden_dim if i == 0 else self.hidden_dim * self.num_heads
            self.gat_layers.append(
                GATConv(
                    in_channels,
                    self.hidden_dim,
                    heads=self.num_heads,
                    dropout=self.dropout,
                    concat=True
                )
            )
        
        # Final projection to single dimension per node
        final_dim = self.hidden_dim * self.num_heads
        self.final_proj = nn.Linear(final_dim, self.hidden_dim)
        
        # Scoring head with attention
        self.attention = nn.MultiheadAttention(
            embed_dim=self.hidden_dim,
            num_heads=4,
            dropout=self.dropout,
            batch_first=True
        )
        
        self.scorer = nn.Sequential(
            nn.Linear(self.hidden_dim, self.hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(self.dropout),
            nn.Linear(self.hidden_dim // 2, 1),
            nn.Sigmoid()
        )
        
        self._init_weights()
    
    def _init_weights(self):
        """Initialize model weights."""
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.xavier_uniform_(module.weight)
                if module.bias is not None:
                    nn.init.zeros_(module.bias)
    
    def forward(self, graph: Data) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Forward pass through the model.
        
        Args:
            graph: PyTorch Geometric Data object
            
        Returns:
            Tuple of (coherence_score, node_importances)
        """
        x, edge_index = graph.x, graph.edge_index
        
        # Input projection
        x = self.input_proj(x)
        x = F.relu(x)
        
        # GAT layers
        for gat_layer in self.gat_layers:
            x = gat_layer(x, edge_index)
            x = F.relu(x)
            x = F.dropout(x, p=self.dropout, training=self.training)
        
        # Final projection
        node_features = self.final_proj(x)
        
        # Aggregate with attention (treat as sequence)
        # node_features: [num_nodes, hidden_dim]
        node_features_expanded = node_features.unsqueeze(0)  # [1, num_nodes, hidden_dim]
        
        # Self-attention to get node importances
        attended_features, attention_weights = self.attention(
            node_features_expanded,
            node_features_expanded,
            node_features_expanded
        )
        
        # Extract node importances from attention weights
        # attention_weights: [1, num_heads, num_nodes, num_nodes]
        node_importances = attention_weights.mean(dim=1).mean(dim=1).squeeze(0)  # [num_nodes]
        
        # Pool to get graph-level representation
        # Use mean pooling with attention weighting
        graph_repr = (attended_features.squeeze(0) * node_importances.unsqueeze(1)).mean(dim=0)
        
        # Score
        coherence_score = self.scorer(graph_repr.unsqueeze(0)).squeeze(0).squeeze(0)
        
        return coherence_score, node_importances
    
    def get_edge_importances(self, graph: Data, node_importances: torch.Tensor) -> torch.Tensor:
        """
        Estimate edge importances from node importances.
        
        Args:
            graph: PyTorch Geometric Data object
            node_importances: Node importance scores
            
        Returns:
            Edge importance scores
        """
        edge_index = graph.edge_index
        
        # Simple heuristic: edge importance = average of source and target node importances
        source_importances = node_importances[edge_index[0]]
        target_importances = node_importances[edge_index[1]]
        edge_importances = (source_importances + target_importances) / 2.0
        
        return edge_importances


class CoherenceModel:
    """
    Wrapper class for the Graph Transformer model with initialization and inference.
    """
    
    def __init__(self):
        self.model = None
        self.device = get_device()
        self.input_dim = None
        self._initialized = False
    
    def initialize(self, input_dim: int):
        """Initialize the model with given input dimension."""
        if self._initialized and self.input_dim == input_dim:
            return
        
        self.input_dim = input_dim
        self.model = GraphTransformer(input_dim=input_dim)
        self.model.to(self.device)
        self.model.eval()
        # Disable gradient computation for inference
        for param in self.model.parameters():
            param.requires_grad = False
        self._initialized = True
        
        logger.info(f"Initialized model with input_dim={input_dim} on device={self.device} (memory-optimized)")
    
    def predict(self, graph: Data) -> Tuple[float, torch.Tensor]:
        """
        Predict coherence score for a graph.
        
        Args:
            graph: PyTorch Geometric Data object
            
        Returns:
            Tuple of (coherence_score, node_importances)
        """
        if not self._initialized:
            # Initialize with graph's feature dimension
            self.initialize(graph.x.shape[1] - 1)  # Subtract 1 for entropy feature
        
        # Ensure graph is on CPU for memory efficiency
        if graph.x.device.type != 'cpu':
            graph = graph.to('cpu')
        graph = graph.to(self.device)
        
        with torch.no_grad():  # Disable gradient computation
            score, node_importances = self.model(graph)
            score = float(score.cpu().item())
            node_importances = node_importances.cpu()
        
        # Cleanup
        del graph
        
        return score, node_importances
    
    def get_edge_importances(self, graph: Data, node_importances: torch.Tensor) -> torch.Tensor:
        """Get edge importance scores."""
        graph = graph.to(self.device)
        with torch.no_grad():
            edge_importances = self.model.get_edge_importances(graph, node_importances.to(self.device))
            return edge_importances.cpu()


# Global model instance
_model_instance = None


def get_model_instance() -> CoherenceModel:
    """Get or create global model instance."""
    global _model_instance
    if _model_instance is None:
        _model_instance = CoherenceModel()
    return _model_instance

