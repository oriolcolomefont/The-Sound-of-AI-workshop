# CLAMP Similarity Search Documentation

## Overview
The CLAMP (Cross-modal Language-Music Pre-training) component provides powerful music similarity search capabilities using Microsoft's CLAMP model. It enables both music-to-music and text-to-music similarity searches.

## Features
- Cross-modal similarity search
- Embedding generation for music pieces
- Efficient nearest neighbor search
- Support for multiple similarity metrics

## Architecture

### Model Details
- Base model: CLAMP-small-512
- Embedding dimension: 512
- Supports both ABC notation and MIDI input
- Pre-trained on large-scale music-text pairs

### Pipeline
1. Input Processing
   - ABC/MIDI parsing
   - Tokenization
   - Feature extraction

2. Embedding Generation
   - Model inference
   - Embedding normalization
   - Caching system

3. Similarity Search
   - Nearest neighbor search
   - Score computation
   - Result ranking

## Usage

### Music-to-Music Search
```bash
python clamp.py -clamp_model_name sander-wood/clamp-small-512 \
                -query_modal music \
                -key_modal music \
                -top_n 3
```

### Text-to-Music Search
```bash
python clamp.py -clamp_model_name sander-wood/clamp-small-512 \
                -query_modal music \
                -key_modal text \
                -top_n 100
```

## Configuration

### Model Parameters
```python
{
    "model_name": "sander-wood/clamp-small-512",
    "embedding_dim": 512,
    "max_sequence_length": 1024,
    "temperature": 0.1,
    "batch_size": 32
}
```

### Search Parameters
```python
{
    "top_k": 100,
    "similarity_threshold": 0.7,
    "metric": "cosine",  # or "euclidean", "dot_product"
    "use_gpu": true
}
```

## Input Formats

### ABC Notation
```
X:1
T:Example Melody
M:4/4
L:1/8
K:C
CDEF GABc|
```

### MIDI Requirements
- Format 0 or 1
- Resolution: 480 ticks per quarter note
- Tempo information required

## Performance Optimization
- Batch processing for multiple queries
- GPU acceleration
- Embedding caching
- Index optimization

## Error Handling
- Input validation
- Model loading fallbacks
- Graceful degradation

## Integration Guide

### Python API
```python
from clamp_search import ClampSearch

searcher = ClampSearch(model_name="sander-wood/clamp-small-512")
results = searcher.search(query="happy melody", mode="text-to-music")
```

### REST API Integration
```python
@app.post("/search")
async def search_endpoint(
    query: str,
    mode: str = "music",
    top_k: int = 10
) -> List[SearchResult]:
    # Implementation
    pass
```

## Troubleshooting

### Common Issues
1. Memory usage with large datasets
2. GPU CUDA errors
3. Input format validation

### Solutions
- Batch size adjustment
- Memory-efficient search
- Input preprocessing 