"""
Coherence scoring module.

Combines model output, similarity heuristics, and graph entropy for final scoring.
Maps to SRS: Scoring and Evaluation Requirements.
"""

import numpy as np
from typing import List, Dict, Tuple
from collections import deque
import logging

from ..models.model import get_model_instance
from ..core.config import settings

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
    # Handle empty or invalid inputs
    if similarity_matrix.size == 0 or entropy_array.size == 0:
        return 0.5  # Default neutral score
    
    # Average similarity (excluding diagonal)
    mask = ~np.eye(similarity_matrix.shape[0], dtype=bool)
    masked_similarities = similarity_matrix[mask]
    
    if masked_similarities.size == 0:
        avg_similarity = 0.5  # Default if no off-diagonal values
    else:
        avg_similarity = float(np.mean(masked_similarities))
        if np.isnan(avg_similarity):
            avg_similarity = 0.5
    
    # Lower entropy = more consistent = higher coherence
    if entropy_array.size > 0:
        avg_entropy = float(np.mean(entropy_array))
        if np.isnan(avg_entropy) or avg_entropy < 0:
            avg_entropy = 0.0
        # Normalize entropy (rough estimate: max entropy ~ log(num_nodes))
        max_possible_entropy = np.log(similarity_matrix.shape[0] + 1)
        normalized_entropy = avg_entropy / max_possible_entropy if max_possible_entropy > 0 else 0
        entropy_score = 1.0 - min(normalized_entropy, 1.0)
    else:
        entropy_score = 0.5
    
    # Combine: weighted average
    heuristic_score = 0.7 * avg_similarity + 0.3 * entropy_score
    
    # Ensure valid number
    result = min(max(heuristic_score, 0.0), 1.0)
    if np.isnan(result) or not np.isfinite(result):
        return 0.5  # Fallback to neutral score
    
    return result


# Calibration buffer for optional min-max normalization
_score_window = deque(maxlen=100)


def _calibrate_score(raw_score: float) -> float:
    """Apply lightweight calibration using a rolling min-max window."""
    _score_window.append(raw_score)
    if len(_score_window) < 5:
        return raw_score
    s_min = min(_score_window)
    s_max = max(_score_window)
    if s_max <= s_min:
        return raw_score
    scaled = (raw_score - s_min) / (s_max - s_min)
    # Blend to avoid oscillations
    return 0.7 * raw_score + 0.3 * float(scaled)


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
    
    # Find edges and score by entropy-weighted weakness
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            sim = similarity_matrix[i, j]
            avg_entropy = (entropy_array[i] + entropy_array[j]) / 2.0
            weakness = (1.0 - sim)
            disruption_score = float(avg_entropy * weakness)
            
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
        # Clearer reasons
        reason = "Weak discourse linkage"
        if disc["similarity"] < 0.3:
            reason = "Abrupt topic transition"
        elif disc["similarity"] < 0.5:
            reason = "Semantic drift"
        
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
        if np.isnan(model_score) or not np.isfinite(model_score):
            model_score = None  # Invalid model score, fall back to heuristic
        else:
            if settings.OPTIMIZED_MODE:
                mean_entropy = float(np.mean(entropy_array)) if entropy_array.size > 0 else 0.0
                if np.isnan(mean_entropy):
                    mean_entropy = 0.0
                final_score = 0.8 * model_score + 0.2 * (1.0 - mean_entropy)
            else:
                final_score = 0.7 * model_score + 0.3 * heuristic_score
    
    if model_score is None:
        final_score = heuristic_score
    
    # Ensure valid score
    if np.isnan(final_score) or not np.isfinite(final_score):
        final_score = heuristic_score  # Fallback to heuristic
    
    # Optional calibration for smoother output
    if settings.OPTIMIZED_MODE:
        final_score = _calibrate_score(float(final_score))
        if np.isnan(final_score) or not np.isfinite(final_score):
            final_score = heuristic_score

    # Identify disruptions
    disruption_report = identify_disruptions(similarity_matrix, entropy_array)

    # Final validation
    final_score = float(final_score)
    if np.isnan(final_score) or not np.isfinite(final_score):
        final_score = 0.5  # Ultimate fallback
    
    return final_score, disruption_report


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

