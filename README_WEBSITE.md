# SatyaScan Website

## Overview
A professional, modern website with 3D animations for SatyaScan - an AI-powered news verification system. The website features an interactive interface with Three.js-powered 3D background animations and seamless integration with the ML backend.

## Features

### Frontend
- **3D Animated Background**: Interactive particle system using Three.js
- **Modern UI Design**: Professional gradient-based design with smooth animations
- **Responsive Layout**: Works seamlessly on desktop, tablet, and mobile devices
- **Real-time Analysis**: Instant feedback with detailed results visualization
- **Smooth Scrolling**: Elegant navigation with smooth scroll effects
- **Interactive Elements**: Hover effects, parallax scrolling, and fade-in animations

### Backend
- **Flask API**: RESTful API endpoints for news analysis
- **Model Integration**: Seamless connection to the trained ML models
- **Error Handling**: Robust error handling and user feedback
- **Health Check**: API health monitoring endpoint

## File Structure

```
multilingual_fake_news/
├── app.py                 # Flask backend server
├── templates/
│   └── index.html        # Main HTML page
├── static/
│   ├── css/
│   │   └── style.css     # Styling and animations
│   └── js/
│       └── main.js       # 3D animations and API integration
└── requirements.txt      # Updated with Flask dependencies
```

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure your ML models are trained and saved in the `models/` directory:
   - `news_svm_calibrated.pkl`
   - `tfidf_word.pkl`
   - `tfidf_char.pkl`
   - `num_scaler.pkl`
   - `feature_names.pkl`
   - `model_metadata.pkl`

## Running the Website

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## API Endpoints

### POST `/api/analyze`
Analyzes a news article for fake news detection.

**Request Body:**
```json
{
    "text": "Your news article text here...",
    "language": "auto"  // or "en", "hi", "mr"
}
```

**Response:**
```json
{
    "is_fake": false,
    "confidence": 0.95,
    "detected_language": "en",
    "sentiment": {
        "sentiment": 0.2,
        "subjectivity": 0.4
    },
    "top_features": [
        ["feature_name", 0.123]
    ],
    "translation": null
}
```

### GET `/api/health`
Health check endpoint to verify server and model status.

**Response:**
```json
{
    "status": "healthy",
    "models_loaded": true
}
```

## Website Sections

1. **Hero Section**: Eye-catching introduction with statistics and call-to-action
2. **Analysis Section**: Main interface for analyzing news articles
3. **Features Section**: Showcase of system capabilities
4. **About Section**: Information about the technology stack

## 3D Animations

The website features a stunning 3D particle system background:
- 2000+ animated particles
- Interactive mouse movement effects
- Smooth camera rotations
- Color-coded particles (primary, secondary, accent colors)
- Performance-optimized rendering

## Customization

### Colors
Edit the CSS variables in `static/css/style.css`:
```css
:root {
    --primary-color: #6366f1;
    --secondary-color: #ec4899;
    --accent-color: #06b6d4;
    /* ... */
}
```

### 3D Particles
Adjust particle settings in `static/js/main.js`:
```javascript
const particleCount = 2000;  // Number of particles
const material = new THREE.PointsMaterial({
    size: 3,  // Particle size
    opacity: 0.8  // Particle opacity
});
```

## Browser Compatibility

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Performance

- Optimized Three.js rendering
- Lazy loading of animations
- Efficient API calls
- Responsive image handling

## Troubleshooting

### Models Not Loading
- Ensure all model files exist in the `models/` directory
- Check file permissions
- Verify model files are not corrupted

### 3D Animation Not Showing
- Check browser console for errors
- Ensure Three.js CDN is accessible
- Verify WebGL support in your browser

### API Errors
- Check Flask server logs
- Verify model files are loaded correctly
- Ensure all dependencies are installed

## Future Enhancements

- [ ] Dark/Light theme toggle
- [ ] Batch analysis feature
- [ ] URL input for direct article fetching
- [ ] Export results as PDF
- [ ] Real-time news monitoring
- [ ] Browser extension integration

## License

Same as the main project (MIT License).

