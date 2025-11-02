"""
Graph construction module.

Builds semantic + discourse graphs from sentence embeddings with entropy features.
Maps to SRS: Graph Construction and Feature Engineering Requirements.
"""

import numpy as np
import torch
from torch_geometric.data import Data
from typing import List, Tuple, Optional
import logging
from scipy.spatial.distance import cosine
from scipy.stats import entropy as scipy_entropy

from ..models.embeddings import embed_sentences

logger = logging.getLogger(__name__)


def cosine_similarity(emb1: np.ndarray, emb2: np.ndarray) -> float:
    """Compute cosine similarity between two embeddings."""
    # Normalized embeddings, so cosine similarity is just dot product
    return float(np.dot(emb1, emb2))


def compute_local_entropy(embeddings: np.ndarray, similarities: np.ndarray, node_idx: int) -> float:
    """
    Compute local entropy for a node based on neighbor similarities.
    
    Args:
        embeddings: All sentence embeddings
        similarities: Similarity matrix (symmetric)
        node_idx: Index of the current node
        
    Returns:
        Shannon entropy value
    """
    # Get similarities to all neighbors
    neighbor_sims = similarities[node_idx, :]
    
    # Filter self-similarity and normalize
    neighbor_sims = neighbor_sims.copy()
    neighbor_sims[node_idx] = 0  # Remove self-connection
    
    # Normalize to probabilities
    total = np.sum(neighbor_sims)
    if total == 0:
        return 0.0
    
    probs = neighbor_sims / total
    probs = probs[probs > 0]  # Remove zeros for entropy calculation
    
    if len(probs) == 0:
        return 0.0
    
    return float(scipy_entropy(probs))


def build_graph(
    sentences: List[str],
    embeddings: np.ndarray,
    discourse_markers: List[List[str]],
    similarity_threshold: float = 0.0,
    discourse_boost: float = 0.1
) -> Tuple[Data, np.ndarray, np.ndarray]:
    """
    Build graph from sentences and embeddings.
    
    Args:
        sentences: List of sentence strings
        embeddings: Sentence embeddings array (num_sentences, embedding_dim)
        discourse_markers: List of discourse markers per sentence
        similarity_threshold: Minimum similarity to create edge
        discourse_boost: Additional weight boost for discourse-marked edges
        
    Returns:
        Tuple of (PyG Data object, similarity_matrix, entropy_array)
    """
    num_sentences = len(sentences)
    
    if num_sentences == 0:
        raise ValueError("Cannot build graph from empty sentences")
    
    if num_sentences == 1:
        # Single node graph
        # Convert embeddings to float32 if needed
        if embeddings.dtype == np.float16:
            embeddings = embeddings.astype(np.float32)
        return Data(
            x=torch.tensor(embeddings, dtype=torch.float32),
            edge_index=torch.zeros((2, 0), dtype=torch.long),
            edge_attr=torch.zeros((0, 1), dtype=torch.float32)
        ), np.array([[1.0]]), np.array([0.0])
    
    # Build similarity matrix (ensure embeddings are float32 for precision)
    embeddings_for_sim = embeddings.astype(np.float32) if embeddings.dtype == np.float16 else embeddings
    similarity_matrix = np.zeros((num_sentences, num_sentences), dtype=np.float32)
    
    for i in range(num_sentences):
        for j in range(i + 1, num_sentences):
            sim = cosine_similarity(embeddings_for_sim[i], embeddings_for_sim[j])
            
            # Boost if discourse markers present in either sentence
            if discourse_markers[i] or discourse_markers[j]:
                sim += discourse_boost
                sim = min(sim, 1.0)  # Cap at 1.0
            
            similarity_matrix[i, j] = sim
            similarity_matrix[j, i] = sim
    
    # Set diagonal to 1.0 (self-similarity)
    np.fill_diagonal(similarity_matrix, 1.0)
    
    # Compute entropy for each node
    entropy_array = np.array([
        compute_local_entropy(embeddings, similarity_matrix, i)
        for i in range(num_sentences)
    ])
    
    # Build edge list (only above threshold)
    edge_list = []
    edge_weights = []
    
    for i in range(num_sentences):
        for j in range(i + 1, num_sentences):
            if similarity_matrix[i, j] >= similarity_threshold:
                edge_list.append([i, j])
                edge_list.append([j, i])  # Undirected graph
                weight = float(similarity_matrix[i, j])
                edge_weights.append(weight)
                edge_weights.append(weight)
    
    if not edge_list:
        # Create minimum spanning connections
        for i in range(num_sentences - 1):
            edge_list.append([i, i + 1])
            edge_list.append([i + 1, i])
            weight = float(similarity_matrix[i, i + 1])
            edge_weights.append(weight)
            edge_weights.append(weight)
    
    # Convert embeddings to float32 for tensor operations (float16 can cause issues)
    if embeddings.dtype == np.float16:
        embeddings = embeddings.astype(np.float32)
    
    # Combine embeddings with entropy as additional feature
    node_features = np.hstack([
        embeddings,
        entropy_array.reshape(-1, 1)
    ]).astype(np.float32)  # Ensure float32
    
    # Convert to PyTorch tensors (CPU only, memory-efficient)
    edge_index = torch.tensor(edge_list, dtype=torch.long, device='cpu').t().contiguous()
    edge_attr = torch.tensor(edge_weights, dtype=torch.float32, device='cpu').unsqueeze(1)
    x = torch.tensor(node_features, dtype=torch.float32, device='cpu')
    
    graph_data = Data(x=x, edge_index=edge_index, edge_attr=edge_attr)
    
    logger.debug(f"Built graph with {num_sentences} nodes and {len(edge_list) // 2} edges")
    
    return graph_data, similarity_matrix, entropy_array

