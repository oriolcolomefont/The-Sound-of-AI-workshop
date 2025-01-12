# Symbolic Soroll Documentation

Welcome to the comprehensive documentation for the Symbolic Soroll Music Information Retrieval system.

## Components

### Core Components
- [API Documentation](api.md) - FastAPI backend server documentation
- [Client Documentation](client.md) - Next.js frontend application documentation
- [CLAMP Documentation](clamp.md) - Music similarity search documentation
- [Text-to-Music Documentation](text-to-music.md) - Natural language to music generation
- [ABC Utilities Documentation](abc-utils.md) - ABC notation tools and utilities

### Additional Resources
- [Setup Guide](../setup/SETUP.md) - Environment setup instructions
- [Contributing Guidelines](CONTRIBUTING.md) - Guidelines for contributors
- [API Reference](API_REFERENCE.md) - Detailed API endpoint documentation

## Quick Start

1. **Setup Environment**
   ```bash
   # Clone repository
   git clone https://github.com/yourusername/symbolic-soroll
   cd symbolic-soroll
   
   # Setup environment
   conda env create -f environment.yml
   conda activate soroll
   ```

2. **Start Services**
   ```bash
   # Start API server
   cd api
   uvicorn main:app --reload

   # Start client
   cd client
   npm install
   npm run dev
   ```

3. **Access Application**
   - Frontend: http://localhost:3000
   - API Documentation: http://localhost:8000/docs

## Architecture Overview

```
Symbolic Soroll
├── Frontend (Next.js)
│   └── Interactive UI for music generation and analysis
├── Backend (FastAPI)
│   ├── Music Generation API
│   ├── Similarity Search API
│   └── Format Conversion API
└── Core Components
    ├── CLAMP (Similarity Search)
    ├── Text-to-Music Generator
    └── ABC Utilities
```

## Common Use Cases

1. **Generate Music from Text**
   ```bash
   cd text-to-music
   python run_inference.py -num_tunes 3
   ```

2. **Find Similar Melodies**
   ```bash
   cd clamp
   python clamp.py -query_modal music -key_modal music
   ```

3. **Convert Formats**
   ```bash
   cd abc-utils
   python convert.py input.abc output.mid
   ```

## Development Workflow

1. **Code Organization**
   - Follow component-based architecture
   - Maintain separation of concerns
   - Use consistent coding style

2. **Testing**
   - Write unit tests for new features
   - Run integration tests before merging
   - Maintain test coverage

3. **Documentation**
   - Update component docs for changes
   - Keep API documentation current
   - Add examples for new features

## Troubleshooting

### Common Issues
1. Environment setup problems
2. Model loading errors
3. API connection issues

### Solutions
- Check environment variables
- Verify model downloads
- Confirm service status

## Support

- GitHub Issues: [Report bugs](https://github.com/yourusername/symbolic-soroll/issues)
- Discussions: [Ask questions](https://github.com/yourusername/symbolic-soroll/discussions)
- Wiki: [Additional resources](https://github.com/yourusername/symbolic-soroll/wiki)

## License
This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details. 