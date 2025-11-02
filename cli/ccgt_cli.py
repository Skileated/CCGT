#!/usr/bin/env python3
"""
CCGT Command-Line Interface.

CLI tool for evaluating text coherence from command line.
Maps to SRS: CLI Tools and Batch Processing.
"""

import sys
import json
from pathlib import Path
import typer
from typing import Optional

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.pipeline.preprocess import preprocess_text
from app.models.embeddings import embed_sentences
from app.pipeline.graph_builder import build_graph
from app.pipeline.scorer import score_text
from app.services.explainability import build_graph_for_visualization
from app.models.model import get_model_instance

app = typer.Typer()


@app.command()
def evaluate(
    file: Optional[Path] = typer.Option(None, "--file", "-f", help="Input text file"),
    text: Optional[str] = typer.Option(None, "--text", "-t", help="Input text directly"),
    save_graph: Optional[Path] = typer.Option(None, "--save-graph", "-g", help="Save graph JSON to file"),
    visualize: bool = typer.Option(False, "--visualize", "-v", help="Include graph visualization data"),
):
    """
    Evaluate text coherence.
    
    Either --file or --text must be provided.
    """
    # Get input text
    if file:
        if not file.exists():
            typer.echo(f"Error: File not found: {file}", err=True)
            raise typer.Exit(1)
        input_text = file.read_text(encoding='utf-8')
    elif text:
        input_text = text
    else:
        typer.echo("Error: Either --file or --text must be provided", err=True)
        raise typer.Exit(1)
    
    if not input_text.strip():
        typer.echo("Error: Input text is empty", err=True)
        raise typer.Exit(1)
    
    try:
        typer.echo("Processing text...")
        
        # Preprocess
        sentences, discourse_markers = preprocess_text(input_text)
        typer.echo(f"Segmented into {len(sentences)} sentences")
        
        if len(sentences) < 1:
            typer.echo("Error: Text must contain at least one sentence", err=True)
            raise typer.Exit(1)
        
        # Generate embeddings
        typer.echo("Generating embeddings...")
        embeddings = embed_sentences(sentences)
        
        # Build graph
        typer.echo("Building graph...")
        graph, similarity_matrix, entropy_array = build_graph(
            sentences,
            embeddings,
            discourse_markers
        )
        
        # Score
        typer.echo("Computing coherence score...")
        coherence_score, disruption_report = score_text(graph, similarity_matrix, entropy_array)
        
        # Output results
        typer.echo("\n" + "="*50)
        typer.echo("COHERENCE EVALUATION RESULTS")
        typer.echo("="*50)
        typer.echo(f"\nCoherence Score: {coherence_score:.4f}")
        typer.echo(f"Coherence Percent: {int(coherence_score * 100)}%")
        
        if disruption_report:
            typer.echo(f"\nDisruption Report ({len(disruption_report)} issues):")
            for i, disruption in enumerate(disruption_report, 1):
                typer.echo(f"\n  {i}. Sentence {disruption['from_idx'] + 1} → Sentence {disruption['to_idx'] + 1}")
                typer.echo(f"     Reason: {disruption['reason']}")
                typer.echo(f"     Score: {disruption['score']:.4f}")
        
        # Save graph if requested
        if save_graph or visualize:
            typer.echo("\nGenerating graph visualization data...")
            try:
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
            
            if save_graph:
                save_graph.parent.mkdir(parents=True, exist_ok=True)
                with open(save_graph, 'w', encoding='utf-8') as f:
                    json.dump(graph_data, f, indent=2)
                typer.echo(f"\nGraph saved to: {save_graph}")
        
        typer.echo("\n" + "="*50)
        
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        import traceback
        traceback.print_exc()
        raise typer.Exit(1)


@app.command()
def batch(
    input_file: Path = typer.Argument(..., help="Input file with one paragraph per line"),
    output_file: Optional[Path] = typer.Option(None, "--output", "-o", help="Output JSON file"),
):
    """
    Batch evaluate multiple paragraphs from a file.
    
    Input file should have one paragraph per line.
    """
    if not input_file.exists():
        typer.echo(f"Error: File not found: {input_file}", err=True)
        raise typer.Exit(1)
    
    paragraphs = input_file.read_text(encoding='utf-8').strip().split('\n')
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    
    typer.echo(f"Processing {len(paragraphs)} paragraphs...")
    
    results = []
    
    for i, paragraph in enumerate(paragraphs, 1):
        typer.echo(f"\n[{i}/{len(paragraphs)}] Processing...")
        try:
            sentences, discourse_markers = preprocess_text(paragraph)
            
            if len(sentences) < 1:
                results.append({
                    "text": paragraph[:50] + "..." if len(paragraph) > 50 else paragraph,
                    "coherence_score": 0.0,
                    "coherence_percent": 0,
                    "error": "No sentences found"
                })
                continue
            
            embeddings = embed_sentences(sentences)
            graph, similarity_matrix, entropy_array = build_graph(
                sentences,
                embeddings,
                discourse_markers
            )
            coherence_score, _ = score_text(graph, similarity_matrix, entropy_array)
            
            results.append({
                "text": paragraph[:50] + "..." if len(paragraph) > 50 else paragraph,
                "coherence_score": float(coherence_score),
                "coherence_percent": int(coherence_score * 100)
            })
            
            typer.echo(f"  Score: {coherence_score:.4f}")
            
        except Exception as e:
            typer.echo(f"  Error: {e}")
            results.append({
                "text": paragraph[:50] + "..." if len(paragraph) > 50 else paragraph,
                "coherence_score": 0.0,
                "coherence_percent": 0,
                "error": str(e)
            })
    
    # Save results
    if output_file:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({"results": results, "total_processed": len(results)}, f, indent=2)
        typer.echo(f"\nResults saved to: {output_file}")
    else:
        typer.echo("\nResults:")
        typer.echo(json.dumps({"results": results, "total_processed": len(results)}, indent=2))


if __name__ == "__main__":
    app()

