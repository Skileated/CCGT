# Changelog

All notable changes to CCGT will be documented in this file.

## [1.0.0] - 2024-01-01

### Added

- Complete backend API with FastAPI
- Graph Transformer model for coherence scoring
- Sentence-BERT integration for embeddings
- Graph construction with semantic similarity and discourse markers
- Frontend dashboard with D3.js visualization
- CLI tool for batch evaluation
- Docker containerization
- Comprehensive test suite
- CI/CD with GitHub Actions
- JWT authentication
- Explainability endpoints
- Batch evaluation API
- Demo notebook
- Example data and sample outputs

### Technical Details

- Backend: FastAPI, PyTorch, PyTorch Geometric, sentence-transformers
- Frontend: React, TypeScript, Tailwind CSS, D3.js
- Performance: ≤ 2s inference for 500 words on moderate CPU
- Security: JWT-based API authentication

### Known Limitations

- Optimized for English text
- Fixed discourse marker list
- CPU-based inference by default
