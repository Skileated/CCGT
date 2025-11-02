"""
Unit tests for the preprocessing pipeline.

Maps to SRS: Testing Requirements.
"""

import pytest
import numpy as np
from app.pipeline.preprocess import (
    segment_sentences,
    detect_discourse_markers,
    normalize_text,
    preprocess_text
)
from app.models.embeddings import embed_sentences
from app.pipeline.graph_builder import build_graph
from app.pipeline.scorer import score_text


def test_segment_sentences():
    """Test sentence segmentation."""
    text = "This is sentence one. This is sentence two! Is this sentence three?"
    sentences = segment_sentences(text)
    assert len(sentences) >= 3
    assert "sentence one" in sentences[0].lower()
    assert "sentence two" in sentences[1].lower()


def test_detect_discourse_markers():
    """Test discourse marker detection."""
    assert "however" in detect_discourse_markers("However, this is a test.")
    assert "therefore" in detect_discourse_markers("This is a test. Therefore, we proceed.")
    assert len(detect_discourse_markers("This is a regular sentence.")) == 0


def test_normalize_text():
    """Test text normalization."""
    text = "This   has    multiple    spaces."
    normalized = normalize_text(text)
    assert "  " not in normalized  # No double spaces


def test_preprocess_text():
    """Test complete preprocessing."""
    text = "This is sentence one. However, this is sentence two. Therefore, we have sentence three."
    sentences, discourse_markers = preprocess_text(text)
    
    assert len(sentences) >= 3
    assert len(discourse_markers) == len(sentences)
    # Check that discourse markers are detected
    assert any(markers for markers in discourse_markers)


def test_embed_sentences():
    """Test embedding generation."""
    sentences = ["This is a test sentence.", "This is another sentence."]
    embeddings = embed_sentences(sentences)
    
    assert embeddings.shape[0] == len(sentences)
    assert embeddings.shape[1] > 0  # Has embedding dimension
    assert isinstance(embeddings, np.ndarray)


def test_build_graph():
    """Test graph construction."""
    sentences = [
        "This is sentence one.",
        "This is sentence two.",
        "This is sentence three."
    ]
    
    embeddings = embed_sentences(sentences)
    discourse_markers = [[], [], []]
    
    graph, similarity_matrix, entropy_array = build_graph(
        sentences,
        embeddings,
        discourse_markers
    )
    
    assert graph.x.shape[0] == len(sentences)
    assert similarity_matrix.shape == (len(sentences), len(sentences))
    assert len(entropy_array) == len(sentences)
    assert graph.edge_index.shape[0] == 2  # Source and target


def test_score_text():
    """Test coherence scoring."""
    sentences = [
        "The field of NLP has advanced significantly.",
        "Machine learning models can understand text.",
        "Coherence is an important aspect of quality."
    ]
    
    embeddings = embed_sentences(sentences)
    discourse_markers = [[], [], []]
    
    graph, similarity_matrix, entropy_array = build_graph(
        sentences,
        embeddings,
        discourse_markers
    )
    
    coherence_score, disruption_report = score_text(
        graph,
        similarity_matrix,
        entropy_array
    )
    
    assert 0.0 <= coherence_score <= 1.0
    assert isinstance(disruption_report, list)


def test_full_pipeline():
    """Test complete pipeline integration."""
    text = """
    Natural language processing has advanced significantly.
    Machine learning models can now understand text.
    However, evaluating quality remains challenging.
    Coherence is one important aspect.
    """
    
    sentences, discourse_markers = preprocess_text(text)
    assert len(sentences) >= 3
    
    embeddings = embed_sentences(sentences)
    assert embeddings.shape[0] == len(sentences)
    
    graph, similarity_matrix, entropy_array = build_graph(
        sentences,
        embeddings,
        discourse_markers
    )
    
    coherence_score, disruption_report = score_text(
        graph,
        similarity_matrix,
        entropy_array
    )
    
    assert 0.0 <= coherence_score <= 1.0

