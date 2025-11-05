"""
Sentence embedding module.

Wraps sentence-transformers for generating semantic embeddings.
Maps to SRS: Embedding Generation Requirements.
"""

import numpy as np
import torch
from typing import List, Optional
import logging
from pathlib import Path
import pickle
import hashlib

from ..core.config import settings, get_device

logger = logging.getLogger(__name__)

# Global model instance (lazy loaded)
_model = None


def get_model():
    """Lazy load the sentence transformer model."""
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            
            model_name = settings.MODEL_NAME
            cache_dir = Path(settings.MODEL_CACHE_DIR)
            cache_dir.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"Loading model: {model_name}")
            device = get_device()
            _model = SentenceTransformer(model_name, device=device, cache_folder=str(cache_dir))
            # Force CPU and enable memory-efficient mode
            if device == "cpu":
                _model.eval()  # Set to evaluation mode
                # Disable gradient computation
                for param in _model.parameters():
                    param.requires_grad = False
            logger.info(f"Model loaded on device: {device} (memory-optimized)")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    return _model


class EmbeddingCache:
    """Simple file-based cache for embeddings."""
    
    def __init__(self, cache_dir: str = None):
        self.cache_dir = Path(cache_dir or settings.EMBEDDING_CACHE_DIR)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache = {}
        self._load_cache()
    
    def _get_key(self, text: str) -> str:
        """Generate cache key from text."""
        # Use SHA1 to reduce collision risk
        return hashlib.sha1(text.encode('utf-8')).hexdigest()
    
    def _get_cache_path(self, key: str) -> Path:
        """Get cache file path."""
        return self.cache_dir / f"{key}.pkl"
    
    def _load_cache(self):
        """Load existing cache files."""
        if not settings.CACHE_EMBEDDINGS:
            return
        
        try:
            for cache_file in self.cache_dir.glob("*.pkl"):
                with open(cache_file, 'rb') as f:
                    data = pickle.load(f)
                    self.cache[data['key']] = data['embedding']
        except Exception as e:
            logger.warning(f"Failed to load embedding cache: {e}")
    
    def get(self, text: str) -> Optional[np.ndarray]:
        """Get cached embedding if available."""
        if not settings.CACHE_EMBEDDINGS:
            return None
        
        key = self._get_key(text)
        
        # Check memory cache
        if key in self.cache:
            return self.cache[key]
        
        # Check file cache
        cache_path = self._get_cache_path(key)
        if cache_path.exists():
            try:
                with open(cache_path, 'rb') as f:
                    data = pickle.load(f)
                    embedding = data['embedding']
                    self.cache[key] = embedding
                    return embedding
            except Exception as e:
                logger.warning(f"Failed to load from cache file: {e}")
        
        return None
    
    def set(self, text: str, embedding: np.ndarray):
        """Cache an embedding."""
        if not settings.CACHE_EMBEDDINGS:
            return
        
        key = self._get_key(text)
        self.cache[key] = embedding
        
        cache_path = self._get_cache_path(key)
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump({'key': key, 'embedding': embedding}, f)
        except Exception as e:
            logger.warning(f"Failed to save to cache file: {e}")


# Global cache instance
_embedding_cache = EmbeddingCache() if settings.CACHE_EMBEDDINGS else None


def embed_sentences(sentences: List[str], batch_size: Optional[int] = None) -> np.ndarray:
    """
    Generate embeddings for a list of sentences.
    
    Args:
        sentences: List of sentence strings
        batch_size: Batch size for embedding generation
        
    Returns:
        Numpy array of shape (num_sentences, embedding_dim)
    """
    if not sentences:
        return np.array([])
    
    batch_size = batch_size or settings.BATCH_SIZE
    
    # Check cache for each sentence
    cached_embeddings = {}
    uncached_indices = []
    
    if _embedding_cache:
        for i, sentence in enumerate(sentences):
            cached = _embedding_cache.get(sentence)
            if cached is not None:
                cached_embeddings[i] = cached
            else:
                uncached_indices.append(i)
    else:
        uncached_indices = list(range(len(sentences)))
    
    # Generate embeddings for uncached sentences
    embeddings_list = [None] * len(sentences)
    
    # Place cached embeddings
    for i, emb in cached_embeddings.items():
        embeddings_list[i] = emb
    
    # Generate embeddings for uncached
    if uncached_indices:
        uncached_sentences = [sentences[i] for i in uncached_indices]
        model = get_model()
        
        # Batch process with memory efficiency
        all_embeddings = []
        for i in range(0, len(uncached_sentences), batch_size):
            batch = uncached_sentences[i:i + batch_size]
            with torch.no_grad():  # Disable gradient computation
                batch_embeddings = model.encode(
                    batch,
                    convert_to_numpy=True,
                    show_progress_bar=False,
                    normalize_embeddings=True
                )
            # Convert to float16 if enabled
            if settings.USE_FLOAT16:
                batch_embeddings = batch_embeddings.astype(np.float16)
            all_embeddings.append(batch_embeddings)
        
        uncached_embeddings = np.vstack(all_embeddings)
        
        # Cache and place embeddings
        for idx, embedding in zip(uncached_indices, uncached_embeddings):
            embeddings_list[idx] = embedding
            if _embedding_cache:
                _embedding_cache.set(sentences[idx], embedding)
    
    # Stack into single array
    embeddings = np.vstack(embeddings_list)

    # Enforce dtype and normalization under optimized mode
    if settings.OPTIMIZED_MODE:
        # Use float32 for numeric stability downstream
        if embeddings.dtype != np.float32:
            embeddings = embeddings.astype(np.float32)
        # Explicit L2 normalization to ensure exact cosine behavior
        norms = np.linalg.norm(embeddings, ord=2, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        embeddings = embeddings / norms
    
    return embeddings

