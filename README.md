# 🍉 AI Fruit Ninja - Hand Gesture Controlled Game

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8.0-red.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.9-orange.svg)](https://google.github.io/mediapipe/)

> An interactive computer vision game that uses real-time hand tracking for gesture-based fruit slicing. Built with MediaPipe, OpenCV, and Pygame.

---

## 🎯 Overview

AI Fruit Ninja is a real-time computer vision application that demonstrates practical implementation of hand tracking and gesture recognition. Players use their index finger to slice falling fruits while avoiding bombs, showcasing the integration of machine learning models with interactive game mechanics.

### Key Highlights

- **Real-time Hand Tracking**: Uses MediaPipe's pre-trained models for accurate hand landmark detection
- **Computer Vision Integration**: Processes webcam feed at 60 FPS for smooth gameplay
- **Gesture Recognition**: Detects slicing motions through finger position tracking
- **Physics Simulation**: Implements realistic projectile motion and gravity
- **Interactive Gameplay**: Responsive scoring system with visual feedback

---

## ✨ Features

### Core Functionality

- ✅ **Real-time Hand Detection**: MediaPipe-powered hand tracking with 21 landmark points
- ✅ **Gesture-Based Controls**: Slice fruits using index finger movements
- ✅ **Bomb Avoidance System**: Penalty mechanism for hitting bombs
- ✅ **Lives System**: Three-strike gameplay mechanic
- ✅ **Score Tracking**: Real-time score display with high score persistence
- ✅ **Visual Effects**: Trail effects and smooth animations
- ✅ **Live Camera Feed**: Picture-in-picture webcam display

### Technical Features

- 60 FPS Gameplay
- Collision Detection Algorithm
- Physics Engine (Gravity & Velocity)
- State Management (Menu, Playing, Paused, Game Over)
- Modular Architecture

---

## 🎥 Demo

### Gameplay Preview

<img width="700" height="660" src="https://github.com/user-attachments/assets/14b822fb-cb97-41c8-af15-117d27a56f28" />
<img width="700" height="550" src="https://github.com/user-attachments/assets/3dbbc398-0318-45c4-b97b-2e09f96c5218" />
<img width="700" height="660" src="https://github.com/user-attachments/assets/4f65cbaa-af26-4877-b47e-fe0bc7031dea" />
<img width="700" height="660" alt="image" src="https://github.com/user-attachments/assets/b60e3f1c-233b-4036-9122-53543fe6dca1" />


### How to Play!
1. Show your hand to the camera
2. Use your index finger to slice fruits
3. Avoid bombs (💣)
4. Score as many points as possible!

---

## 📦 Installation

### Prerequisites

- Python 3.8 - 3.11 (MediaPipe not compatible with Python 3.12+)
- Webcam/Camera
- Windows 10/11, macOS, or Linux
- 4GB RAM minimum

### Step-by-Step Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/fruit-ninja-ai.git
cd fruit-ninja-ai
```

#### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Verify Installation

```bash
python -c "import cv2, mediapipe, pygame; print('✅ All dependencies installed successfully!')"
```

---

## 🎮 Usage

### Running the Game

```bash
python main.py
```

### Game Controls

| Key | Action |
|-----|--------|
| **SPACE** | Start game from menu |
| **P** | Pause/Resume game |
| **R** | Restart after game over |
| **Q** | Quit to desktop |
| **Index Finger** | Slice fruits (in-game) |

### Gameplay Tips

- 🔆 **Good Lighting**: Ensure adequate lighting for better hand detection
- 📏 **Optimal Distance**: Sit 2-3 feet from the camera
- 🖐️ **Hand Position**: Keep hand flat with fingers clearly visible
- 🎯 **Smooth Movements**: Use controlled, deliberate slicing motions


## 📁 Project Structure

```
fruit-ninja-ai/
│
├── main.py                    # Main game loop and entry point
├── hand_detector.py           # MediaPipe hand tracking wrapper
├── game_objects.py            # Fruit and Trail classes
├── config.py                  # Game configuration and constants
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── LICENSE                    # MIT License
├── .venv/                     # Virtual environment (not committed)
└── .gitignore                # Git ignore rules
```

### File Descriptions

#### **main.py** - Game Engine (350+ lines)
- Initializes Pygame and camera
- Manages game states (menu, playing, game over)
- Handles game loop at 60 FPS
- Processes user input and events
- Renders UI and game objects

#### **hand_detector.py** - Computer Vision Module
- Wraps MediaPipe Hands API
- Processes video frames for hand detection
- Extracts 21 hand landmark coordinates
- Provides finger position tracking
- Maps camera coordinates to game screen

#### **game_objects.py** - Game Logic
- `Fruit` class: Manages fruit physics, rendering, and collision
- `Trail` class: Creates visual trail effect for finger movement
- Collision detection algorithms
- Slice animation logic

#### **config.py** - Configuration
- Game constants (screen size, FPS, spawn rate)
- Fruit types and point values
- Physics parameters (gravity, velocity)
- Color definitions

---

## 🔍 How It Works

### System Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Webcam    │─────▶│   OpenCV     │─────▶│  MediaPipe  │
│   Input     │      │  Processing  │      │ Hand Model  │
└─────────────┘      └──────────────┘      └─────────────┘
                                                    │
                                                    ▼
                                            ┌─────────────┐
                                            │  Hand       │
                                            │  Landmarks  │
                                            └─────────────┘
                                                    │
                                                    ▼
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Pygame    │◀─────│   Game       │◀─────│  Coordinate │
│   Render    │      │   Logic      │      │  Mapping    │
└─────────────┘      └──────────────┘      └─────────────┘
```

### Processing Pipeline

1. **Video Capture** (60 FPS)
   - OpenCV captures webcam frames (640x480)
   - Frames flipped horizontally for mirror effect

2. **Hand Detection**
   - MediaPipe processes RGB frames
   - Detects up to 1 hand with 21 landmarks
   - Confidence threshold: 70%

3. **Coordinate Extraction**
   - Index finger tip (landmark #8) tracked
   - Camera coordinates mapped to game screen (1280x720)
   - Smoothing applied for stable tracking

4. **Collision Detection**
   - Euclidean distance calculated between finger and fruits
   - Collision threshold: 50 pixels
   - Triggers slice animation and score update

5. **Game Logic**
   - Fruits spawn at bottom with random trajectories
   - Physics updated each frame (gravity: 0.5, velocity: -10 to -15)
   - Score calculated based on fruit type
   - Lives decremented on missed fruits or bomb hits

6. **Rendering**
   - Pygame draws all game objects (fruits, UI, effects)
   - Camera feed displayed in top-right corner
   - Trail effect rendered from finger movement history

### Key Algorithms

#### Distance-Based Collision Detection
```python
distance = sqrt((fruit.x - finger.x)² + (fruit.y - finger.y)²)
if distance < 50:  # threshold
    collision = True
```

#### Projectile Motion Physics
```python
velocity_y += gravity  # Acceleration (0.5)
position_x += velocity_x  # Horizontal movement
position_y += velocity_y  # Vertical movement with gravity
```

---

## 🛠️ Technologies Used

| Technology | Purpose | Version |
|------------|---------|---------|
| **Python** | Core Programming Language | 3.10.11 |
| **MediaPipe** | Hand Tracking & Landmark Detection | 0.10.9 |
| **OpenCV** | Computer Vision & Image Processing | 4.8.0 |
| **Pygame** | Game Development Framework | 2.5.0 |
| **NumPy** | Numerical Computations | 1.24.3 |

### Why These Technologies?

- **MediaPipe**: Google's production-ready ML solution with 95%+ hand tracking accuracy
- **OpenCV**: Industry-standard library for real-time computer vision operations
- **Pygame**: Lightweight, cross-platform game engine with simple API
- **Python**: Rapid prototyping with extensive ML/CV ecosystem

---

## 🚀 Deployment

### Creating Executable File

#### Using PyInstaller

```bash
# Install PyInstaller
pip install pyinstaller

# Create single executable
pyinstaller --onefile --windowed --name="FruitNinjaAI" main.py

# Output will be in dist/ folder
```

#### Distribution Package

Create a professional distribution folder:

```
FruitNinjaAI-v1.0/
│
├── FruitNinjaAI.exe          # Executable
├── README.txt                # User instructions
└── LICENSE.txt               # License information
```

---

## 🔮 Future Enhancements

### Planned Features

- [ ] **Sound Effects**: Add slicing sounds and background music
- [ ] **Difficulty Levels**: Easy, Medium, Hard modes
- [ ] **Power-ups**: Slow motion, double points, freeze time
- [ ] **Combo System**: Multiplier for consecutive slices
- [ ] **Leaderboard**: Persistent high score database
- [ ] **Two-Hand Mode**: Support for both hands simultaneously
- [ ] **Special Fruits**: Golden fruits with bonus points
- [ ] **Mobile Version**: Port to Android/iOS

### Technical Improvements

- [ ] Performance optimization with multi-threading
- [ ] Custom gesture recognition model
- [ ] Web deployment using TensorFlow.js
- [ ] Analytics dashboard for gameplay statistics

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Standards

- Follow PEP 8 style guidelines
- Add docstrings to functions
- Include comments for complex logic
- Test thoroughly before submitting

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---


## 🙏 Acknowledgments

- **Google MediaPipe Team** - For excellent hand tracking models
- **OpenCV Community** - For comprehensive computer vision tools
- **Pygame Developers** - For accessible game development framework
- **Fruit Ninja (Halfbrick Studios)** - Original game inspiration

---

## 📊 System Requirements

### Minimum Requirements
- OS: Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- Processor: Intel Core i3 or equivalent
- RAM: 4GB
- Webcam: 720p (30 FPS)
- Python: 3.8 - 3.11

### Recommended Requirements
- OS: Windows 11, macOS 12+, Ubuntu 22.04+
- Processor: Intel Core i5 or equivalent
- RAM: 8GB
- Webcam: 1080p (60 FPS)
- Python: 3.10

---

## 🐛 Troubleshooting

### Common Issues

**Camera not detected:**
```python
# Try different camera indices in main.py
self.cap = cv2.VideoCapture(0)  # Try 0, 1, or 2
```

**Low FPS / Lag:**
- Close other applications
- Ensure good lighting
- Reduce game resolution in config.py

**Hand not detected:**
- Improve lighting conditions
- Keep hand within camera frame
- Maintain 2-3 feet distance from camera

**Import errors:**
```bash
# Reinstall dependencies
pip uninstall opencv-python mediapipe pygame
pip install -r requirements.txt
```

---

## 📚 Learning Resources

### Computer Vision
- [MediaPipe Documentation](https://google.github.io/mediapipe/)
- [OpenCV Tutorials](https://docs.opencv.org/master/d9/df8/tutorial_root.html)

### Game Development
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Game Programming Patterns](https://gameprogrammingpatterns.com/)

### Python Best Practices
- [PEP 8 Style Guide](https://pep8.org/)
- [Real Python Tutorials](https://realpython.com/)

---

<div align="center">

**⭐ Star this repo if you found it helpful!**

Made with ❤️ and Python 🐍

[⬆ Back to Top](#-ai-fruit-ninja---hand-gesture-controlled-game)

</div>
