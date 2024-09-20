# Sleeping Detection in Cars

## Overview

The **Sleeping Detection in Cars** project aims to monitor driver alertness by detecting whether an individual is sleeping or drowsy while inside a car. This real-time application utilizes facial landmarks and eye blink detection to assess the driver's state, providing alerts when necessary to enhance safety.

## Key Features

- **Real-Time Detection**: Continuously analyzes video input to assess the driver's alertness.
- **Status Indicators**: Detects three states: "Sleeping", "Drowsy", and "Active", with corresponding visual indicators.
- **Sound Alerts**: Plays alert sounds when the driver is detected as sleeping or drowsy.

## Tools and Technologies Used

- **Programming Language**: Python 3.x
- **Libraries**:
  - OpenCV: For video capture and image processing.
  - Mediapipe: For facial landmark detection.
  - NumPy: For numerical operations.
  - Playsound: To play audio alerts.
  
## Methodology

### 1. Initialization
- Initializes the Mediapipe Face Mesh model to detect facial landmarks in real-time.
- Sets up the camera for video capture.

### 2. Eye Blink Detection
- Uses specific facial landmarks to determine if the eyes are open, semi-open, or closed.
- Calculates the blink ratio to assess the state of alertness:
  - Eyes open
  - Eyes semi-open (drowsy)
  - Eyes closed (sleeping)

### 3. Status Tracking
- Tracks the status of the driver using counters:
  - Increments the "sleep" counter when eyes are closed.
  - Increments the "drowsy" counter when eyes are semi-open.
  - Increments the "active" counter when eyes are open.
  
### 4. Visual Feedback
- Displays the current status on the screen with appropriate color coding:
  - Red for "Sleeping"
  - Orange for "Drowsy"
  - Green for "Active"
  
### 5. Audio Alerts
- Plays specific alert sounds when the driver's state changes to "Sleeping" or "Drowsy".

