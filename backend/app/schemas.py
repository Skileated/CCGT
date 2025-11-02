"""
Pydantic schemas for request/response validation.

Defines data models for API endpoints.
Maps to SRS: API Specification and Data Models.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class EvaluateRequest(BaseModel):
    """Request schema for text evaluation."""
    text: str = Field(..., description="Paragraph text to evaluate", min_length=10)
    options: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional parameters like visualization flags"
    )


class DisruptionItem(BaseModel):
    """Represents a weak link in the text."""
    from_idx: int = Field(..., description="Source sentence index")
    to_idx: int = Field(..., description="Target sentence index")
    reason: str = Field(..., description="Reason for disruption (e.g., 'low_similarity')")
    score: float = Field(..., description="Disruption score (lower = more disruptive)")


class GraphNode(BaseModel):
    """Graph node representation."""
    id: int = Field(..., description="Node ID (sentence index)")
    text_snippet: str = Field(..., description="Sentence text")
    entropy: Optional[float] = Field(None, description="Local entropy metric")
    importance_score: Optional[float] = Field(None, description="Node importance score")
    embedding_dim_reduced: Optional[List[float]] = Field(None, description="2D reduced embedding for visualization")


class GraphEdge(BaseModel):
    """Graph edge representation."""
    source: int = Field(..., description="Source node ID")
    target: int = Field(..., description="Target node ID")
    weight: float = Field(..., description="Edge weight (similarity/discourse strength)")
    discourse_marker: Optional[str] = Field(None, description="Discourse marker if present")
    reason: Optional[str] = Field(None, description="Reason for edge strength")


class GraphData(BaseModel):
    """Complete graph structure."""
    nodes: List[GraphNode] = Field(..., description="List of graph nodes")
    edges: List[GraphEdge] = Field(..., description="List of graph edges")


class EvaluateResponse(BaseModel):
    """Response schema for text evaluation."""
    coherence_score: float = Field(..., description="Coherence score (0-1)", ge=0, le=1)
    coherence_percent: int = Field(..., description="Coherence as percentage (0-100)")
    disruption_report: List[DisruptionItem] = Field(..., description="List of weak links")
    graph: Optional[GraphData] = Field(None, description="Graph structure for visualization")


class BatchEvaluateRequest(BaseModel):
    """Request schema for batch evaluation."""
    texts: List[str] = Field(..., description="List of paragraphs to evaluate", min_items=1)
    options: Optional[Dict[str, Any]] = Field(default=None)


class BatchEvaluateItem(BaseModel):
    """Single item in batch response."""
    text: str = Field(..., description="Original text")
    coherence_score: float = Field(..., description="Coherence score (0-1)")
    coherence_percent: int = Field(..., description="Coherence as percentage")


class BatchEvaluateResponse(BaseModel):
    """Response schema for batch evaluation."""
    results: List[BatchEvaluateItem] = Field(..., description="Evaluation results")
    total_processed: int = Field(..., description="Number of texts processed")


class HealthResponse(BaseModel):
    """Health check response."""
    model_config = ConfigDict(protected_namespaces=())  # Resolve conflict with "model_" namespace
    
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    is_model_loaded: bool = Field(..., description="Whether ML model is loaded", serialization_alias="model_loaded")

