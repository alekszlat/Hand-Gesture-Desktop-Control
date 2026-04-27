# Hand Gesture Desktop Control for Linux Mint

A desktop application that uses computer vision and hand gestures to control the Linux desktop environment.  
The goal of this project is to allow users to move the cursor, interact with windows, and launch applications using hand movements captured through a webcam.

## Overview

This project explores gesture-based human-computer interaction on **Linux Mint**.  
The application detects a user's hand through a camera feed, interprets specific gestures, and maps them to desktop actions such as:

- Moving the mouse cursor
- Clicking or dragging
- Opening applications
- Interacting with browser windows
- Triggering custom desktop shortcuts

The project is being designed with a strong focus on:

- Clear modular architecture
- Real-time hand tracking
- Safe and reliable gesture recognition
- Linux desktop integration
- Future extensibility for additional gestures and actions

## Project Goals

The main objectives of this project are:

- Build a hand-controlled desktop interaction system for Linux Mint
- Detect and track hand landmarks in real time
- Translate hand movement into desktop input
- Support gesture-based launching of applications
- Enable browser and window interaction through gestures
- Create a maintainable and scalable foundation for future development

## Planned Features

### Phase 1
- Webcam capture
- Real-time hand detection
- Hand landmark tracking
- Simple cursor movement based on hand position
- Debug visualization for tracking accuracy

### Phase 2
- Gesture smoothing and stability improvements
- Click gesture detection
- Basic calibration flow
- Reduced false positives

### Phase 3
- Application launching through gestures
- Window interaction support
- Browser control experiments
- Gesture-to-action mapping system

### Phase 4
- Improved desktop UI
- User settings and configuration
- Startup integration
- Packaging and distribution

## Target Platform

- **Operating System:** Linux Mint (for initial development and testing)
- **Desktop Environment:** Primarily X11-based workflow for initial development
- **Hardware:** Standard laptop or desktop webcam

## Architecture Direction

The system is planned around the following high-level components:

- **Capture Layer**  
  Responsible for reading frames from the webcam.

- **Hand Tracking Layer**  
  Detects the hand and extracts landmarks.

- **Gesture Interpretation Layer**  
  Converts tracked hand movement into meaningful gesture states.

- **Action Layer**  
  Maps recognized gestures to desktop actions.

- **Desktop Integration Layer**  
  Communicates with the Linux desktop to move the cursor, launch apps, and manage interactions.

## Technology Direction

The current project direction includes exploring:

- **OpenCV** for camera input and frame processing
- **MediaPipe** for hand landmark detection
- **Linux desktop automation tools** for cursor and application control
- **Optional desktop UI frameworks** for future configuration panels and controls

## Current Status

This project is currently in the early prototyping and architecture stage.

Initial focus:
- Define the technical structure
- Select the right frameworks
- Build a small proof of concept
- Validate hand tracking and basic desktop control on Linux Mint

## Development Philosophy

This project is being developed with the following principles:

- Start small and validate each layer independently
- Prioritize reliability over feature count
- Separate gesture recognition from desktop actions
- Build for maintainability first, then optimize
- Keep the project modular so future expansion is easier

## Future Ideas

Possible future extensions include:

- Multi-gesture profiles
- Gesture customization
- System tray integration
- Voice + gesture hybrid control
- Wayland compatibility research
- Accessibility-focused interaction modes

## Repository Structure

This structure may evolve as development progresses.

```text
.
├── README.md
├── src/
└──  tests/