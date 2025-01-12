# Client Documentation

## Overview
The Next.js frontend provides an intuitive interface for interacting with the MIR system's capabilities. It features a modern, responsive design with real-time music generation and visualization.

## Features

### Music Generation Interface
- Text-to-music generation form
- Real-time ABC notation preview
- Interactive music player
- Generation parameter controls

### Similarity Search
- Drag-and-drop melody input
- Visual similarity results
- Audio playback of results
- Cross-modal search interface

### Visualization Components
- ABC notation renderer
- Piano roll display
- Waveform visualization
- Music score display

## Component Structure
```
client/
├── components/        # Reusable React components
│   ├── MusicPlayer/  # Audio playback
│   ├── NotationView/ # ABC rendering
│   └── Controls/     # Parameter controls
├── pages/            # Next.js pages
├── styles/           # CSS modules
└── utils/            # Helper functions
```

## State Management
- React Context for global state
- Local component state for UI
- API integration hooks

## Development

### Setup
```bash
cd client
npm install
npm run dev
```

### Building
```bash
npm run build
npm start
```

### Environment Variables
Create `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GA_ID=your-analytics-id
```

## Component API Reference

### MusicPlayer
```typescript
interface MusicPlayerProps {
  abc: string;           // ABC notation
  autoPlay?: boolean;    // Auto-start playback
  onPlay?: () => void;   // Playback callbacks
  onStop?: () => void;
}
```

### NotationView
```typescript
interface NotationViewProps {
  notation: string;      // ABC notation
  interactive?: boolean; // Enable interaction
  scale?: number;        // Display scale
}
```

### Controls
```typescript
interface ControlsProps {
  onParameterChange: (param: string, value: number) => void;
  disabled?: boolean;
  presets?: Preset[];
}
```

## Styling
- Tailwind CSS for utility classes
- CSS modules for component styles
- Theme customization via Tailwind config

## Performance Optimization
- Dynamic imports for heavy components
- Image optimization
- API response caching
- Memoized components 