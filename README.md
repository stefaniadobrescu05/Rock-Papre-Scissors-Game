# Rock-Papre-Scissors-Game

An interactive Rock–Paper–Scissors game controlled by real-time hand-gesture recognition with your webcam.

## What this project does
- Detects your hand gesture (rock, paper, scissors) using MediaPipe Hands and OpenCV.
- Mirrors the camera feed for a natural experience and draws UI overlays (score, ROI box, instructions, results).
- Plays rounds against a computer opponent with live scoring and quick feedback.

## Tech stack
- Python 3.10+
- OpenCV (camera capture, drawing UI overlays)
- MediaPipe Hands (gesture/landmark detection)
- NumPy (frames as arrays)

## Setup
1) Create and activate a virtual environment (recommended):
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
```

2) Install dependencies:
```bash
pip install -r requirements.txt
```

## How to run
```bash
python main.py
```

## How to play
- Position your hand inside the on-screen ROI box.
- Make one of the three gestures:
	- Rock: closed fist
	- Paper: open palm (fingers extended)
	- Scissors: index and middle fingers extended in a V
- Press **C** to capture your current gesture and play a round.
- Press **H** to toggle help text.
- Press **Q** to quit.

What you will see
- Top bar: score and instructions (wrapped to fit).
- ROI box: place your hand here; colored outline shows detection status.
- Top-right: real-time detected gesture text or an invalid gesture warning.
- Center-top: round result (Win/Lose/Draw) after you press C.
- Bottom: only the computer move is shown (your move is not shown after capture, per request).

## Notes and tips
- Ensure good lighting and keep your hand inside the ROI box for reliable detection.
- If gestures are not recognized, adjust hand distance/angle and press C again.
- The camera feed is mirrored horizontally to feel natural.

## Project structure (key parts)
- `main.py` — game loop wiring camera, gesture recognition, and UI.
- `responsibilities/camera_utils.py` — camera access, window display, key handling.
- `responsibilities/gesture_recognition.py` — MediaPipe-based gesture detection and classification.
- `responsibilities/ui.py` — all on-screen overlays (score, instructions, ROI, results).
- `responsibilities/game_logic.py` — game rules and winner determination.
- `tests/` — basic tests for game logic.

## Troubleshooting
- Window too small: resize or maximize; the window is resizable (cv2.WINDOW_NORMAL).
- Invalid gesture message: adjust hand pose; ensure the gesture matches rock/paper/scissors.
- Camera not opening: verify another app is not using the webcam and that the correct camera index is used (default 0).

