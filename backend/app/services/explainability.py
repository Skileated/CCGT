"""
Explainability and visualization service.

Generates graph data structures and explanations for visualization.
Maps to SRS: Explainability and Visualization Requirements.
"""

import numpy as np
from sklearn.decomposition import PCA
from typing import List, Dict, Tuple
import logging
import torch

from ..models.model import get_model_instance

logger = logging.getLogger(__name__)


def reduce_embedding_dimensions(embeddings: np.ndarray, n_components: int = 2) -> np.ndarray:
    """
    Reduce embedding dimensions to 2D for visualization.
    
    Args:
        embeddings: Original embeddings (num_nodes, embedding_dim)
        n_components: Target dimension (typically 2)
        
    Returns:
        Reduced embeddings (num_nodes, n_components)
    """
    if embeddings.shape[0] <= 1:
        # Not enough points for PCA
        return np.zeros((embeddings.shape[0], n_components))
    
    if embeddings.shape[1] <= n_components:
        # Already lower dimension
        return embeddings[:, :n_components]
    
    try:
        pca = PCA(n_components=n_components, random_state=42)
        reduced = pca.fit_transform(embeddings)
        return reduced
    except Exception as e:
        logger.warning(f"PCA reduction failed: {e}, using random projection")
        # Fallback: random projection
        np.random.seed(42)
        proj = np.random.randn(embeddings.shape[1], n_components)
        reduced = embeddings @ proj
        return reduced


def generate_explanation_text(disruption: Dict) -> str:
    """Generate human-readable explanation for a disruption."""
    reason = disruption.get("reason", "unknown")
    score = disruption.get("score", 0.0)
    
    explanations = {
        "very_low_similarity": f"Very low semantic similarity ({score:.2f}) between sentences",
        "low_similarity": f"Low semantic similarity ({score:.2f}) between sentences",
        "high_entropy": "High local entropy indicating inconsistent connections",
        "missing_discourse": "Missing discourse markers for transition"
    }
    
    return explanations.get(reason, f"Disruption detected (score: {score:.2f})")


def build_graph_for_visualization(
    sentences: List[str],
    embeddings: np.ndarray,
    similarity_matrix: np.ndarray,
    entropy_array: np.ndarray,
    discourse_markers: List[List[str]],
    disruption_report: List[Dict],
    graph,
    node_importances: np.ndarray = None
) -> Dict:
    """
    Build complete graph structure for frontend visualization.
    
    Args:
        sentences: List of sentence strings
        embeddings: Sentence embeddings
        similarity_matrix: Similarity matrix
        entropy_array: Entropy array
        discourse_markers: Discourse markers per sentence
        disruption_report: List of disruptions
        graph: PyTorch Geometric graph
        node_importances: Optional node importance scores
        
    Returns:
        Dictionary with nodes and edges
    """
    # Reduce embeddings to 2D
    embeddings_2d = reduce_embedding_dimensions(embeddings)
    
    # Get node importances if available
    if node_importances is None:
        try:
            _, node_importances_tensor = get_model_instance().predict(graph)
            # Detach and convert to numpy safely
            if isinstance(node_importances_tensor, torch.Tensor):
                node_importances = node_importances_tensor.detach().cpu().numpy()
            else:
                node_importances = node_importances_tensor
        except Exception as e:
            logger.warning(f"Failed to get node importances, using entropy fallback: {e}")
            # Fallback: use entropy as importance (inverted)
            node_importances = 1.0 / (entropy_array + 0.1)
            node_importances = node_importances / node_importances.max()
    
    # Build nodes
    nodes = []
    for i, sentence in enumerate(sentences):
        # Truncate long sentences for display
        text_snippet = sentence[:100] + "..." if len(sentence) > 100 else sentence
        
        nodes.append({
            "id": i,
            "text_snippet": text_snippet,
            "entropy": float(entropy_array[i]),
            "importance_score": float(node_importances[i]),
            "embedding_dim_reduced": embeddings_2d[i].tolist()
        })
    
    # Build edges
    disruption_set = {(d["from_idx"], d["to_idx"]) for d in disruption_report}
    
    edges = []
    # Safely convert tensors to numpy
    edge_index = graph.edge_index.detach().cpu().numpy()
    edge_weights = graph.edge_attr.detach().cpu().numpy().flatten() if graph.edge_attr is not None else None
    
    for i in range(edge_index.shape[1]):
        source = int(edge_index[0, i])
        target = int(edge_index[1, i])
        
        # Skip duplicate edges (undirected graph)
        if source >= target:
            continue
        
        weight = float(edge_weights[i]) if edge_weights is not None else float(similarity_matrix[source, target])
        
        # Check for discourse markers
        discourse = None
        if discourse_markers[source] or discourse_markers[target]:
            discourse = ", ".join(set(discourse_markers[source] + discourse_markers[target]))
        
        # Check if this is a disruption
        is_disruption = (source, target) in disruption_set or (target, source) in disruption_set
        reason = None
        if is_disruption:
            for d in disruption_report:
                if (d["from_idx"] == source and d["to_idx"] == target) or \
                   (d["from_idx"] == target and d["to_idx"] == source):
                    reason = generate_explanation_text(d)
                    break
        
        edges.append({
            "source": source,
            "target": target,
            "weight": weight,
            "discourse_marker": discourse,
            "reason": reason
        })
    
    return {
        "nodes": nodes,
        "edges": edges
    }

