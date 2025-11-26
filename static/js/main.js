// 3D Background Animation
let scene, camera, renderer, particles, particleSystem;
let mouseX = 0, mouseY = 0;
let windowHalfX = window.innerWidth / 2;
let windowHalfY = window.innerHeight / 2;

// Initialize 3D Scene
function init3D() {
    const canvas = document.getElementById('bg-canvas');
    if (!canvas) return;

    // Scene setup
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1, 1000);
    camera.position.z = 1000;

    // Create particle system
    const particleCount = 2000;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    const color1 = new THREE.Color(0x6366f1); // Primary color
    const color2 = new THREE.Color(0xec4899); // Secondary color
    const color3 = new THREE.Color(0x06b6d4); // Accent color

    for (let i = 0; i < particleCount; i++) {
        const i3 = i * 3;
        
        // Position
        positions[i3] = (Math.random() - 0.5) * 2000;
        positions[i3 + 1] = (Math.random() - 0.5) * 2000;
        positions[i3 + 2] = (Math.random() - 0.5) * 2000;

        // Color
        const colorChoice = Math.random();
        let color;
        if (colorChoice < 0.33) color = color1;
        else if (colorChoice < 0.66) color = color2;
        else color = color3;

        colors[i3] = color.r;
        colors[i3 + 1] = color.g;
        colors[i3 + 2] = color.b;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
        size: 3,
        vertexColors: true,
        transparent: true,
        opacity: 0.8,
        blending: THREE.AdditiveBlending
    });

    particleSystem = new THREE.Points(geometry, material);
    scene.add(particleSystem);

    // Create connecting lines
    const lineGeometry = new THREE.BufferGeometry();
    const linePositions = new Float32Array(particleCount * 3);
    lineGeometry.setAttribute('position', new THREE.BufferAttribute(linePositions, 3));

    const lineMaterial = new THREE.LineBasicMaterial({
        color: 0x6366f1,
        transparent: true,
        opacity: 0.1
    });

    const lines = new THREE.LineSegments(lineGeometry, lineMaterial);
    scene.add(lines);

    // Renderer
    renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);

    // Mouse movement
    document.addEventListener('mousemove', onDocumentMouseMove, false);
    window.addEventListener('resize', onWindowResize, false);

    animate();
}

function onDocumentMouseMove(event) {
    mouseX = (event.clientX - windowHalfX) * 0.05;
    mouseY = (event.clientY - windowHalfY) * 0.05;
}

function onWindowResize() {
    windowHalfX = window.innerWidth / 2;
    windowHalfY = window.innerHeight / 2;

    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function animate() {
    requestAnimationFrame(animate);

    if (particleSystem) {
        particleSystem.rotation.x += 0.0005;
        particleSystem.rotation.y += 0.001;

        // Mouse interaction
        camera.position.x += (mouseX - camera.position.x) * 0.05;
        camera.position.y += (-mouseY - camera.position.y) * 0.05;
        camera.lookAt(scene.position);
    }

    renderer.render(scene, camera);
}

// Initialize 3D on load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init3D);
} else {
    init3D();
}

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Character counter
const textInput = document.getElementById('text-input');
const charCount = document.getElementById('char-count');

if (textInput && charCount) {
    textInput.addEventListener('input', () => {
        charCount.textContent = textInput.value.length;
    });
}

// Analysis functionality
const analyzeBtn = document.getElementById('analyze-btn');
const languageSelect = document.getElementById('language-select');
const resultsContainer = document.getElementById('results');

if (analyzeBtn) {
    analyzeBtn.addEventListener('click', async () => {
        const text = textInput.value.trim();
        const language = languageSelect.value;

        if (!text) {
            alert('Please enter some text to analyze.');
            return;
        }

        // Show loading state
        analyzeBtn.disabled = true;
        analyzeBtn.querySelector('.btn-text').style.display = 'none';
        analyzeBtn.querySelector('.btn-loader').style.display = 'flex';
        resultsContainer.style.display = 'none';

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    language: language
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                if (response.status === 503) {
                    // Models not loaded
                    showError('Models not loaded. Please train the models first by running: python scripts/model_training.py');
                } else {
                    throw new Error(errorData.error || 'Analysis failed');
                }
                return;
            }

            const result = await response.json();
            
            if (result.error) {
                showError(result.error);
                return;
            }
            
            displayResults(result);

        } catch (error) {
            console.error('Error:', error);
            showError('An error occurred during analysis. Please try again.');
        } finally {
            // Reset button state
            analyzeBtn.disabled = false;
            analyzeBtn.querySelector('.btn-text').style.display = 'inline';
            analyzeBtn.querySelector('.btn-loader').style.display = 'none';
        }
    });
}

function displayResults(result) {
    // Show results container
    resultsContainer.style.display = 'block';
    resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    // Verdict
    const verdictBadge = document.getElementById('verdict-badge');
    const verdictText = document.getElementById('verdict-text');
    
    if (result.is_fake) {
        verdictBadge.className = 'verdict-badge fake';
        verdictText.textContent = 'Fake News';
    } else {
        verdictBadge.className = 'verdict-badge genuine';
        verdictText.textContent = 'Genuine News';
    }

    // Confidence
    const confidence = (result.confidence * 100).toFixed(1);
    const confidenceBar = document.getElementById('confidence-bar');
    const confidenceValue = document.getElementById('confidence-value');
    
    confidenceBar.style.width = confidence + '%';
    confidenceValue.textContent = confidence + '%';

    // Language
    const detectedLang = document.getElementById('detected-lang');
    const langMap = {
        'en': 'English',
        'hi': 'Hindi (हिंदी)',
        'mr': 'Marathi (मराठी)',
        'ta': 'Tamil (தமிழ்)',
        'te': 'Telugu (తెలుగు)',
        'bn': 'Bengali (বাংলা)',
        'gu': 'Gujarati (ગુજરાતી)',
        'kn': 'Kannada (ಕನ್ನಡ)',
        'ml': 'Malayalam (മലയാളം)',
        'pa': 'Punjabi (ਪੰਜਾਬੀ)',
        'or': 'Odia (ଓଡ଼ିଆ)',
        'ur': 'Urdu (اردو)',
        'as': 'Assamese (অসমীয়া)'
    };
    detectedLang.textContent = langMap[result.detected_language] || result.detected_language;

    // Sentiment
    const sentiment = document.getElementById('sentiment');
    const sentimentValue = result.sentiment.sentiment;
    let sentimentText = 'Neutral';
    if (sentimentValue > 0.1) sentimentText = 'Positive';
    else if (sentimentValue < -0.1) sentimentText = 'Negative';
    sentiment.textContent = `${sentimentText} (${sentimentValue.toFixed(2)})`;

    // Subjectivity
    const subjectivity = document.getElementById('subjectivity');
    const subjValue = result.sentiment.subjectivity;
    const subjText = subjValue > 0.5 ? 'Highly Subjective' : 'More Objective';
    subjectivity.textContent = `${subjText} (${subjValue.toFixed(2)})`;

    // Translation
    const translationSection = document.getElementById('translation-section');
    const translationText = document.getElementById('translation-text');
    if (result.translation) {
        translationSection.style.display = 'block';
        translationText.textContent = result.translation;
    } else {
        translationSection.style.display = 'none';
    }

    // Features
    const featuresList = document.getElementById('features-list');
    featuresList.innerHTML = '';
    
    if (result.top_features && result.top_features.length > 0) {
        result.top_features.forEach(([feature, importance]) => {
            const li = document.createElement('li');
            const impact = importance > 0 ? 'increases' : 'decreases';
            li.textContent = `'${feature}' ${impact} likelihood of being genuine (weight: ${Math.abs(importance).toFixed(3)})`;
            featuresList.appendChild(li);
        });
    } else {
        const li = document.createElement('li');
        li.textContent = 'Feature importance data not available';
        li.style.opacity = '0.6';
        featuresList.appendChild(li);
    }
}

// Add parallax effect to hero stats
const statCards = document.querySelectorAll('.stat-card');
if (statCards.length > 0) {
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        statCards.forEach((card, index) => {
            // Reduced speed for subtler animation
            const speed = 0.15 + (index * 0.05);
            // Limit maximum translation to prevent excessive movement
            const maxTranslation = 50;
            const translation = Math.min(scrolled * speed, maxTranslation);
            card.style.transform = `translateY(${translation}px)`;
        });
    });
}

// Intersection Observer for fade-in animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe feature cards
document.querySelectorAll('.feature-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(30px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(card);
});

// Error display function
function showError(message) {
    resultsContainer.style.display = 'block';
    resultsContainer.innerHTML = `
        <div class="result-card">
            <div class="result-header">
                <h3>Error</h3>
            </div>
            <div class="result-content">
                <div style="padding: 2rem; text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">⚠️</div>
                    <p style="color: var(--danger-color); font-size: 1.1rem; margin-bottom: 1rem;">${message}</p>
                    <p style="color: var(--text-secondary); font-size: 0.9rem;">
                        To train the models, run:<br>
                        <code style="background: var(--bg-card); padding: 0.5rem 1rem; border-radius: 0.5rem; display: inline-block; margin-top: 0.5rem;">
                            python scripts/model_training.py
                        </code>
                    </p>
                </div>
            </div>
        </div>
    `;
    resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Health check on load
window.addEventListener('load', async () => {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        if (!data.models_loaded) {
            console.warn('Models not loaded. Some features may not work.');
            // Show a banner at the top of the page
            const banner = document.createElement('div');
            banner.style.cssText = `
                position: fixed;
                top: 80px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(239, 68, 68, 0.9);
                color: white;
                padding: 1rem 2rem;
                border-radius: 0.5rem;
                z-index: 999;
                max-width: 90%;
                text-align: center;
                box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            `;
            banner.innerHTML = `
                <strong>⚠️ Models Not Loaded</strong><br>
                <small>Please train models first: <code>python scripts/model_training.py</code></small>
            `;
            document.body.appendChild(banner);
            
            // Auto-hide after 10 seconds
            setTimeout(() => {
                banner.style.opacity = '0';
                banner.style.transition = 'opacity 0.5s';
                setTimeout(() => banner.remove(), 500);
            }, 10000);
        }
    } catch (error) {
        console.error('Health check failed:', error);
    }
});

