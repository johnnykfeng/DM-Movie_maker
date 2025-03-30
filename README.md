# X-Ray Image Processing and Animation Tool

This tool processes X-ray image data and creates animations from structured array files. It provides both command-line and GUI interfaces for data processing and visualization.

## Features

- Process .mat files containing X-ray image data into structured numpy arrays
- Normalize X-ray data using air normalization
- Create MP4 animations from processed data
- GUI interface for easy movie creation
- Support for multiple energy bins (7 bins from 20-120 keV)
- Configurable frame selection, bin selection, and FPS settings

## Installation

1. Clone this repository
2. Install required dependencies:
   ```
   pip install numpy matplotlib scipy tk
   ```
3. Install ffmpeg for video creation

## Usage

### Command Line Interface
Run `main.py` to process data and create animations:
