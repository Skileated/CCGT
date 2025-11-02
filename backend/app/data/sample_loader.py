"""
Sample data loader for testing and demonstrations.

Maps to SRS: Example Data and Testing Requirements.
"""

import json
from pathlib import Path
from typing import List, Dict


def load_example_paragraphs() -> List[Dict]:
    """
    Load example paragraphs from examples/paragraphs.json.
    
    Returns:
        List of example paragraph dictionaries
    """
    examples_path = Path(__file__).parent.parent.parent.parent / "examples" / "paragraphs.json"
    
    if not examples_path.exists():
        return []
    
    with open(examples_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.get("examples", [])


def get_example_by_id(example_id: int) -> Dict:
    """
    Get a specific example paragraph by ID.
    
    Args:
        example_id: Example ID
        
    Returns:
        Example dictionary or empty dict if not found
    """
    examples = load_example_paragraphs()
    for example in examples:
        if example.get("id") == example_id:
            return example
    return {}


def load_sample_output() -> Dict:
    """
    Load sample output JSON for reference.
    
    Returns:
        Sample output dictionary
    """
    sample_path = Path(__file__).parent.parent.parent.parent / "examples" / "sample_output.json"
    
    if not sample_path.exists():
        return {}
    
    with open(sample_path, 'r', encoding='utf-8') as f:
        return json.load(f)

