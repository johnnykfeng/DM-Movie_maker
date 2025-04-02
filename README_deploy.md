
### X-ray detector capture of rotating phantom
<!-- <img src="ASSETS\Screenshot_2025-04-02_154815.png" alt="image" width="400"/> -->
<!-- ![image](ASSETS\Screenshot_2025-04-02_154815.png) -->

This Streamlit web application provides an interactive interface for viewing and analyzing X-ray detector data frames. The app allows users to explore multi-dimensional X-ray data through various visualization tools and controls. The data displayed is the capture of rotating phantom with helical beads on the surface. You can faintly see the smaller beads arranged in a helix, and one larger bead on the surface.

## Features

### X-ray detector image
- Interactive heatmap display of detector frames
- Adjustable color range and colormap selection
- Option to invert colormap
- Configurable figure height

### Analysis Tools
1. **Histogram View**
   - Show distribution of digital pixel values
   - Toggle between linear and logarithmic y-axis
   - Adjustable maximum x and y values

2. **Spatial Analysis**
   - Column-wise average plots
   - Row-wise average plots
   - Individual column/row line profiles
   - Selectable column and row indices

### Display Settings
- Expandable control panel for analysis tools
- Split view layout with heatmap and analysis plots

## Usage

1. Launch the app using Streamlit:
   ```
   streamlit run deploy_dm-frame-viewer.py
   ```

2. Use the sidebar to:
   - Adjust color range
   - Select colormap
   - Toggle colormap inversion

3. Use the main panel to:
   - Toggle different visualization options
   - Adjust analysis parameters
   - View heatmaps and analysis plots
