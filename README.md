# Keep Me Away 👀💻

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-orange)

A smart desktop application that protects your eyes and posture by ensuring you maintain a healthy distance from your screen using AI-powered face detection.

## Features ✨

- 🎯 Real-time face detection using OpenCV's DNN model
- 📏 Automatic distance calibration
- ⏳ 5-second warning before screen blanking
- 🖥️ Full-screen blackout prevention system
- ⚙️ Adjustable proximity threshold
- 📈 Moving average filter for stable detection
- 🖼️ Real-time face area visualization
- 🖱️ Cross-platform compatibility

## Use Cases 👨👩👧👦

### For Parents:
- Protect children's eyesight during online classes
- Prevent kids from leaning too close to tablets/PCs
- Establish healthy screen habits early

### For Remote Workers:
- Maintain proper posture during long work hours
- Reduce digital eye strain
- Create ergonomic workspace reminders

### For Gamers/Streamers:
- Prevent marathon gaming sessions with poor posture
- Maintain optimal viewing distance
- Create healthy streaming environment

### Future Vision (Android App):
📱 Planned mobile version to:
- Protect kids on smartphones/tablets
- Add parental control features
- Implement usage time tracking
- Support multiple user profiles

## Installation 🛠️

### Prerequisites
- Python 3.7+
- Webcam

### Setup
```bash
# Clone repository
git clone https://github.com/yourusername/keep_me_away.git
cd keep_me_away

# Install dependencies
pip install -r requirements.txt

# Download model files
wget https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt
wget https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20180205_fp16/res10_300x300_ssd_iter_140000_fp16.caffemodel
