"""
Text evaluation endpoints.

Maps to SRS: API Evaluation Endpoints.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
import logging

from ...schemas import (
    EvaluateRequest,
    EvaluateResponse,
    BatchEvaluateRequest,
    BatchEvaluateResponse,
    BatchEvaluateItem,
    DisruptionItem,
    GraphNode,
    GraphEdge,
    GraphData
)
from ...pipeline.preprocess import preprocess_text
from ...models.embeddings import embed_sentences
from ...pipeline.graph_builder import build_graph
from ...pipeline.scorer import score_text
from ...services.explainability import build_graph_for_visualization
from ...models.model import get_model_instance

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/evaluate", response_model=EvaluateResponse)
async def evaluate_text(request: EvaluateRequest):
    """
    Evaluate text coherence.
    
    Accepts paragraph text and returns coherence score, disruption report, and optional graph.
    """
    try:
        # Preprocess
        sentences, discourse_markers = preprocess_text(request.text)
        
        if len(sentences) < 1:
            raise HTTPException(status_code=400, detail="Text must contain at least one sentence")
        
        # Generate embeddings
        embeddings = embed_sentences(sentences)
        
        # Build graph
        graph, similarity_matrix, entropy_array = build_graph(
            sentences,
            embeddings,
            discourse_markers
        )
        
        # Score
        coherence_score, disruption_report = score_text(graph, similarity_matrix, entropy_array)
        
        # Build response
        response = EvaluateResponse(
            coherence_score=coherence_score,
            coherence_percent=int(coherence_score * 100),
            disruption_report=[
                DisruptionItem(**d) for d in disruption_report
            ]
        )
        
        # Add graph if visualization requested
        if request.options and request.options.get("visualize", False):
            try:
                # Get node importances
                _, node_importances_tensor = get_model_instance().predict(graph)
                node_importances = node_importances_tensor.numpy()
            except:
                node_importances = None
            
            graph_data = build_graph_for_visualization(
                sentences,
                embeddings,
                similarity_matrix,
                entropy_array,
                discourse_markers,
                disruption_report,
                graph,
                node_importances
            )
            
            response.graph = GraphData(
                nodes=[GraphNode(**node) for node in graph_data["nodes"]],
                edges=[GraphEdge(**edge) for edge in graph_data["edges"]]
            )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Evaluation error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")


@router.post("/batch_evaluate", response_model=BatchEvaluateResponse)
async def batch_evaluate(request: BatchEvaluateRequest):
    """
    Batch evaluate multiple texts.
    
    Accepts a list of paragraphs and returns scores for each.
    """
    results = []
    
    for text in request.texts:
        try:
            # Preprocess
            sentences, discourse_markers = preprocess_text(text)
            
            if len(sentences) < 1:
                # Skip empty texts
                results.append(BatchEvaluateItem(
                    text=text[:50] + "..." if len(text) > 50 else text,
                    coherence_score=0.0,
                    coherence_percent=0
                ))
                continue
            
            # Generate embeddings
            embeddings = embed_sentences(sentences)
            
            # Build graph
            graph, similarity_matrix, entropy_array = build_graph(
                sentences,
                embeddings,
                discourse_markers
            )
            
            # Score
            coherence_score, _ = score_text(graph, similarity_matrix, entropy_array)
            
            results.append(BatchEvaluateItem(
                text=text[:50] + "..." if len(text) > 50 else text,
                coherence_score=coherence_score,
                coherence_percent=int(coherence_score * 100)
            ))
            
        except Exception as e:
            logger.warning(f"Failed to evaluate text in batch: {e}")
            results.append(BatchEvaluateItem(
                text=text[:50] + "..." if len(text) > 50 else text,
                coherence_score=0.0,
                coherence_percent=0
            ))
    
    return BatchEvaluateResponse(
        results=results,
        total_processed=len(results)
    )

