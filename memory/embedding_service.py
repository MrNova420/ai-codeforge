#!/usr/bin/env python3
"""
Embedding Service - Convert text to vector embeddings
Uses sentence-transformers for high-quality embeddings
"""

from typing import List
import numpy as np


class EmbeddingService:
    """
    Service for generating text embeddings.
    
    Uses sentence-transformers which provides quality embeddings
    without requiring API keys or cloud services.
    """
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize embedding service.
        
        Args:
            model_name: sentence-transformers model to use
                       'all-MiniLM-L6-v2' is fast and good quality (default)
                       'all-mpnet-base-v2' is slower but higher quality
        """
        self.model_name = model_name
        self._model = None
        
    def _load_model(self):
        """Lazy load the embedding model."""
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(self.model_name)
            except ImportError:
                raise ImportError(
                    "sentence-transformers not installed. "
                    "Run: pip install sentence-transformers"
                )
    
    def embed_text(self, text: str) -> List[float]:
        """
        Convert text to embedding vector.
        
        Args:
            text: Text to embed
            
        Returns:
            List of floats representing the embedding
        """
        self._load_model()
        embedding = self._model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Convert multiple texts to embeddings (more efficient).
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embeddings
        """
        self._load_model()
        embeddings = self._model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()
    
    def similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity between two texts.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score (0-1, higher is more similar)
        """
        self._load_model()
        emb1 = self._model.encode(text1, convert_to_numpy=True)
        emb2 = self._model.encode(text2, convert_to_numpy=True)
        
        # Cosine similarity
        similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        return float(similarity)
    
    def dimension(self) -> int:
        """Get embedding dimension for this model."""
        self._load_model()
        # Get dimension by embedding a test string
        test_emb = self._model.encode("test", convert_to_numpy=True)
        return len(test_emb)
