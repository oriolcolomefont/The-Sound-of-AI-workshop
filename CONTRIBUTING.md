# Contributing to Symbolic Soroll

Thank you for your interest in contributing to Symbolic Soroll! This document provides guidelines and instructions for contributing to our Music Information Retrieval (MIR) system.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Pull Request Process](#pull-request-process)
- [Development Guidelines](#development-guidelines)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Guidelines](#documentation-guidelines)

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Getting Started

1. **Fork the Repository**
   ```bash
   git clone https://github.com/yourusername/symbolic-soroll.git
   cd symbolic-soroll
   ```

2. **Set Up Development Environment**
   ```bash
   # Python setup
   conda env create -f environment.yml
   conda activate soroll

   # Node.js setup (for frontend)
   cd client
   npm install
   ```

3. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Process

1. **Check Existing Issues**
   - Look for existing issues or create a new one
   - Get approval for major changes before starting

2. **Follow Best Practices**
   - Refer to our [Best Practices Guide](docs/BEST_PRACTICES.md)
   - Follow code style guidelines
   - Write tests for new features

3. **Local Development**
   ```bash
   # Run backend
   cd api
   uvicorn main:app --reload

   # Run frontend
   cd client
   npm run dev
   ```

## Pull Request Process

1. **Before Submitting**
   - Update documentation
   - Add/update tests
   - Run the test suite
   - Update CHANGELOG.md

2. **PR Guidelines**
   - Use our PR template
   - Link related issues
   - Provide clear description
   - Include screenshots for UI changes

3. **PR Title Format**
   ```
   type(scope): brief description

   Types: feat, fix, docs, style, refactor, test, chore
   Example: feat(melody): add transposition support
   ```

## Development Guidelines

### Code Style

#### Python
- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Use type hints
- Maximum line length: 88 characters
- Use Black for formatting

```python
# Good example
from typing import List

def process_melody(abc_notation: str) -> List[str]:
    """Process an ABC notation melody.

    Args:
        abc_notation: Input melody string

    Returns:
        List of processed melody strings
    """
    return [abc_notation]
```

#### TypeScript/React
- Follow Airbnb style guide
- Use functional components
- Implement proper types

```typescript
// Good example
interface Props {
  melody: string;
  onPlay: () => void;
}

const MelodyPlayer: React.FC<Props> = ({ melody, onPlay }) => {
  return <div onClick={onPlay}>{melody}</div>;
};
```

### MIR-Specific Guidelines

1. **Audio Processing**
   - Handle different sample rates
   - Implement proper error checking
   - Use efficient algorithms

2. **Model Management**
   - Version control large files with Git LFS
   - Document model parameters
   - Provide model cards

3. **Data Handling**
   - Validate music notation
   - Handle edge cases
   - Implement proper error recovery

## Testing Guidelines

### Unit Tests
```python
# Example test
def test_melody_transposition():
    input_melody = "K:C\nCDEF|"
    expected = "K:D\nDEF^F|"
    result = transpose_melody(input_melody, semitones=2)
    assert result == expected
```

### Integration Tests
- Test API endpoints
- Test UI components
- Test audio processing pipeline

## Documentation Guidelines

### Code Documentation
- Write clear docstrings
- Document complex algorithms
- Update API documentation

### Component Documentation
- Update component README
- Document new features
- Include usage examples

### API Documentation
- Use OpenAPI/Swagger
- Provide request/response examples
- Document error cases

## Review Process

### Code Review Checklist
1. Code quality
   - Follows style guide
   - No code smells
   - Proper error handling

2. Testing
   - Tests pass
   - Adequate coverage
   - Edge cases covered

3. Documentation
   - Updated docs
   - Clear comments
   - API documentation

### Performance Review
- Check memory usage
- Verify CPU efficiency
- Test with large datasets

## Additional Resources

- [Best Practices Guide](docs/BEST_PRACTICES.md)
- [API Documentation](docs/api.md)
- [Architecture Overview](docs/index.md)

## Questions?

Feel free to:
- Open an issue
- Join our discussions
- Contact maintainers

Thank you for contributing to Symbolic Soroll! 🎵 