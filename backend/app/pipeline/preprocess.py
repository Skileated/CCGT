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
    # Strict normalization: collapse whitespace, unify punctuation spacing
    text = text.replace('\u00A0', ' ')
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r"\s*([,;:])\s*", r"\1 ", text)
    text = re.sub(r"\s*([.!?])\s*", r"\1 ", text)
    text = text.strip()
    return text


def compute_syntactic_features(sentences: List[str]) -> List[float]:
    """
    Compute a simple syntactic distance proxy per sentence using spaCy dependency parse.
    Returns a list where higher values indicate more complex/shifted syntax.
    """
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
    except Exception:
        return [0.0 for _ in sentences]

    scores: List[float] = []
    for sent in sentences:
        doc = nlp(sent)
        deps = [(abs(token.head.i - token.i)) for token in doc if token.head is not token]
        score = float(sum(deps) / len(deps)) if deps else 0.0
        scores.append(score)
    if scores:
        mn, mx = min(scores), max(scores)
        if mx > mn:
            scores = [(s - mn) / (mx - mn) for s in scores]
        else:
            scores = [0.0 for _ in scores]
    return scores


def detect_connective_continuity(sentences: List[str]) -> List[float]:
    """Score continuity based on discourse connectives at sentence starts (0..1)."""
    continuity: List[float] = []
    for i, sent in enumerate(sentences):
        s = sent.strip().lower()
        starts_with = next((m for m in DISCOURSE_MARKERS if s.startswith(m)), None)
        if i == 0:
            continuity.append(1.0)
        else:
            if starts_with in {"however", "nevertheless", "nonetheless", "conversely"}:
                continuity.append(0.4)
            elif starts_with in {"therefore", "thus", "hence", "accordingly"}:
                continuity.append(0.7)
            else:
                continuity.append(0.8)
    return continuity


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

