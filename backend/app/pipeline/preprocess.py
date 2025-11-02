"""
Text preprocessing module.

Handles sentence segmentation, discourse marker detection, and normalization.
Maps to SRS: Preprocessing and Text Analysis Requirements.
"""

import re
from typing import List, Tuple, Set
import logging

logger = logging.getLogger(__name__)

# Discourse markers for English (expanded list)
DISCOURSE_MARKERS: Set[str] = {
    "however", "therefore", "thus", "hence", "meanwhile", "although", "though",
    "consequently", "furthermore", "moreover", "additionally", "nevertheless",
    "nonetheless", "accordingly", "besides", "indeed", "instead", "likewise",
    "otherwise", "similarly", "specifically", "ultimately", "afterward",
    "afterwards", "conversely", "elsewhere", "hereafter", "hitherto",
    "notwithstanding", "previously", "subsequently"
}


def segment_sentences(text: str) -> List[str]:
    """
    Segment text into sentences using spaCy or fallback to regex.
    
    Args:
        text: Input paragraph text
        
    Returns:
        List of sentence strings
    """
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
        
        if sentences:
            return sentences
    except (ImportError, OSError) as e:
        logger.warning(f"spaCy not available, using regex fallback: {e}")
    
    # Regex fallback: split on sentence boundaries
    # Pattern matches: . ! ? followed by space and capital letter or end of string
    pattern = r'(?<=[.!?])\s+(?=[A-Z])|(?<=[.!?])(?=\s*$)'
    sentences = [s.strip() for s in re.split(pattern, text) if s.strip()]
    
    return sentences


def detect_discourse_markers(sentence: str) -> List[str]:
    """
    Detect discourse markers in a sentence.
    
    Args:
        sentence: Input sentence
        
    Returns:
        List of detected discourse markers
    """
    sentence_lower = sentence.lower()
    detected = []
    
    for marker in DISCOURSE_MARKERS:
        # Match whole words only
        pattern = r'\b' + re.escape(marker) + r'\b'
        if re.search(pattern, sentence_lower):
            detected.append(marker)
    
    return detected


def normalize_text(text: str) -> str:
    """
    Basic text normalization.
    
    Args:
        text: Raw text
        
    Returns:
        Normalized text
    """
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Trim
    text = text.strip()
    return text


def preprocess_text(text: str) -> Tuple[List[str], List[List[str]]]:
    """
    Complete preprocessing pipeline.
    
    Args:
        text: Raw paragraph text
        
    Returns:
        Tuple of (sentences, discourse_markers_per_sentence)
    """
    text = normalize_text(text)
    sentences = segment_sentences(text)
    discourse_markers = [detect_discourse_markers(sent) for sent in sentences]
    
    logger.debug(f"Segmented into {len(sentences)} sentences")
    
    return sentences, discourse_markers

