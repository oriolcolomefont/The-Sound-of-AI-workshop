# API Documentation

## Overview
The FastAPI backend server handles all music generation, analysis, and processing requests. It serves as the bridge between the frontend client and the various MIR models and utilities.

## API Endpoints

### Music Generation
- `POST /api/generate/text-to-music`
  - Input: Text description
  - Output: Generated ABC notation
  - Parameters:
    - `text`: String description of desired music
    - `num_tunes`: Number of variations to generate
    - `temperature`: Controls randomness (0.0-1.0)

- `POST /api/generate/tunesformer`
  - Input: Generation parameters
  - Output: Generated ABC notation
  - Parameters:
    - `max_patch`: Maximum patch number
    - `top_p`, `top_k`: Sampling parameters
    - `temperature`: Controls variation

### Similarity Search
- `POST /api/similarity/search`
  - Input: Query melody (ABC notation)
  - Output: Similar melodies
  - Parameters:
    - `query`: ABC notation string
    - `top_n`: Number of results
    - `mode`: 'music' or 'text'

### Format Conversion
- `POST /api/convert/mxl-to-abc`
  - Input: MusicXML file
  - Output: ABC notation
  - Parameters:
    - `measures`: Number of measures
    - `channels`: MIDI channels to include

## Authentication
- Bearer token authentication required for all endpoints
- API keys managed through environment variables

## Error Handling
- Standard HTTP status codes
- Detailed error messages in response body
- Rate limiting implemented

## Development Setup
```bash
cd api
pip install -r requirements.txt
uvicorn main:app --reload
```

## Environment Variables
```
OPENAI_API_KEY=your_key_here
MODEL_PATH=/path/to/models
MAX_REQUEST_SIZE=10MB
``` 