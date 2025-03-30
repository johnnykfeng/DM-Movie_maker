import streamlit as st
import numpy as np
import plotly.express as px
from modules import create_plotly_heatmaps, create_histogram
import pandas as pd
import time

st.set_page_config(layout="wide")

st.title("DM Frame-by-Frame Animation")
with st.sidebar:
    npy_path = st.text_input("Enter the path to the .npy file", value=r"DATA\ANIMATIONS\1_cylinder_0.1Cu_13p8Al_10mA_4000_frames_0.001_resolution_20PE_normalized.npy")
    frame_time = st.number_input("Frame time (ms)", value=10, min_value=5, max_value=1000)
    full_speed = st.checkbox("Full speed", value=False)


frame_num_container = st.empty()
col1, col2 = st.columns(2)
with col1:
    container1 = st.empty()
with col2:
    container2 = st.empty()

npy_data = np.load(npy_path)
n_bins = npy_data.shape[0]
n_total_frames = npy_data.shape[1]

with st.sidebar:
    st.write(f"**Total bins:** {n_bins}")
    st.write(f"**Total frames:** {n_total_frames}")

    # Create a dropdown for bin selection
    bin_selector = st.selectbox(
        'Select a bin number',
        range(n_bins),
        format_func=lambda x: f'Bin {x}'
    )

    fig_height = st.slider("Select the height of the figure", min_value=100, max_value=1000, value=600)
    
    st.subheader("Histogram settings")
    max_y_value = st.number_input("Max y value", value=500, min_value=100, max_value=1000)
    max_x_value = st.number_input("Max x value", value=2.0, min_value=1.0, max_value=30.0)

# Get min and max values across all data for this bin
all_frame_data = npy_data[bin_selector, :]['DM_pixel_data']
data_min = float(np.min(all_frame_data))
data_max = float(np.percentile(all_frame_data, 99))*2

for frame in range(n_total_frames):
    frame_num_container.write(f"Frame {frame}")
    if not full_speed:
        time.sleep(frame_time/1000)

    filtered_data = npy_data[bin_selector, frame]['DM_pixel_data']

    fig = create_plotly_heatmaps(filtered_data, color_range=[data_min, data_max])
    fig.update_layout(height=fig_height)

    fig_histogram = create_histogram(filtered_data, max_y_value=max_y_value, max_x_value=max_x_value)

    container1.plotly_chart(fig)
    container2.plotly_chart(fig_histogram)











