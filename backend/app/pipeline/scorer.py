"""
Coherence scoring module.

Combines model output, similarity heuristics, and graph entropy for final scoring.
Maps to SRS: Scoring and Evaluation Requirements.
"""

import numpy as np
from typing import List, Dict, Tuple
import logging

from ..models.model import get_model_instance

logger = logging.getLogger(__name__)


def compute_heuristic_score(similarity_matrix: np.ndarray, entropy_array: np.ndarray) -> float:
    """
    Compute heuristic coherence score from similarity and entropy.
    
    Args:
        similarity_matrix: Pairwise similarity matrix
        entropy_array: Local entropy for each node
        
    Returns:
        Heuristic score in [0, 1]
    """
    # Average similarity (excluding diagonal)
    mask = ~np.eye(similarity_matrix.shape[0], dtype=bool)
    avg_similarity = float(np.mean(similarity_matrix[mask]))
    
    # Lower entropy = more consistent = higher coherence
    avg_entropy = float(np.mean(entropy_array))
    # Normalize entropy (rough estimate: max entropy ~ log(num_nodes))
    max_possible_entropy = np.log(similarity_matrix.shape[0] + 1)
    normalized_entropy = avg_entropy / max_possible_entropy if max_possible_entropy > 0 else 0
    entropy_score = 1.0 - min(normalized_entropy, 1.0)
    
    # Combine: weighted average
    heuristic_score = 0.7 * avg_similarity + 0.3 * entropy_score
    
    return min(max(heuristic_score, 0.0), 1.0)


def identify_disruptions(
    similarity_matrix: np.ndarray,
    entropy_array: np.ndarray,
    top_k: int = 5
) -> List[Dict]:
    """
    Identify weak links (disruptions) in the text.
    
    Args:
        similarity_matrix: Pairwise similarity matrix
        entropy_array: Local entropy for each node
        top_k: Number of disruptions to return
        
    Returns:
        List of disruption dictionaries
    """
    num_nodes = similarity_matrix.shape[0]
    disruptions = []
    
    # Find edges with lowest similarity
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            sim = similarity_matrix[i, j]
            # Combine similarity and entropy to get disruption score
            avg_entropy = (entropy_array[i] + entropy_array[j]) / 2.0
            disruption_score = (1.0 - sim) * (1.0 + avg_entropy)
            
            disruptions.append({
                "from_idx": i,
                "to_idx": j,
                "similarity": sim,
                "disruption_score": disruption_score
            })
    
    # Sort by disruption score (highest = most disruptive)
    disruptions.sort(key=lambda x: x["disruption_score"], reverse=True)
    
    # Return top_k
    result = []
    for disc in disruptions[:top_k]:
        reason = "low_similarity"
        if disc["similarity"] < 0.3:
            reason = "very_low_similarity"
        elif disc["similarity"] < 0.5:
            reason = "low_similarity"
        
        result.append({
            "from_idx": disc["from_idx"],
            "to_idx": disc["to_idx"],
            "reason": reason,
            "score": disc["similarity"]
        })
    
    return result


def compute_coherence_score(
    graph,
    similarity_matrix: np.ndarray,
    entropy_array: np.ndarray,
    model_score: float = None
) -> Tuple[float, List[Dict]]:
    """
    Compute final coherence score combining model and heuristics.
    
    Args:
        graph: PyTorch Geometric Data object
        similarity_matrix: Pairwise similarity matrix
        entropy_array: Local entropy array
        model_score: Model prediction (if available)
        
    Returns:
        Tuple of (coherence_score, disruption_report)
    """
    # Compute heuristic score
    heuristic_score = compute_heuristic_score(similarity_matrix, entropy_array)
    
    # Combine with model score if available
    if model_score is not None:
        # Weighted combination: trust model more
        final_score = 0.7 * model_score + 0.3 * heuristic_score
    else:
        final_score = heuristic_score
    
    # Identify disruptions
    disruption_report = identify_disruptions(similarity_matrix, entropy_array)
    
    return float(final_score), disruption_report


def score_text(
    graph,
    similarity_matrix: np.ndarray,
    entropy_array: np.ndarray
) -> Tuple[float, List[Dict]]:
    """
    Main scoring function that uses the model if available.
    
    Args:
        graph: PyTorch Geometric Data object
        similarity_matrix: Similarity matrix
        entropy_array: Entropy array
        
    Returns:
        Tuple of (coherence_score, disruption_report)
    """
    model_instance = get_model_instance()
    
    try:
        # Try to get model prediction
        model_score, _ = model_instance.predict(graph)
        logger.debug(f"Model score: {model_score:.3f}")
    except Exception as e:
        logger.warning(f"Model prediction failed, using heuristics only: {e}")
        model_score = None
    
    return compute_coherence_score(graph, similarity_matrix, entropy_array, model_score)

