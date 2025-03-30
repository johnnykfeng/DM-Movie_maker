import streamlit as st
import numpy as np
import plotly.express as px
from modules import create_plotly_heatmaps, create_histogram
import pandas as pd
import time

st.set_page_config(layout="wide")

st.title("DM Frame Viewer")
with st.sidebar:
    npy_path = st.text_input("Enter the path to the .npy file", value=r"DATA\ANIMATIONS\1_cylinder_0.1Cu_13p8Al_10mA_4000_frames_0.001_resolution_20PE_normalized.npy")


# frame_num_container = st.empty()
# col1, col2 = st.columns(2)
# with col1:
#     container1 = st.empty()
# with col2:
#     container2 = st.empty()
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

    # Create a slider for frame selection
    frame_selector = st.number_input("Select a frame number", 
                                     min_value=0, 
                                     max_value=n_total_frames-1, 
                                     value=0, step=1)
    
st.write(f"**Selected bin:** {bin_selector}")
st.write(f"**Selected frame:** {frame_selector}")

# Get min and max values across all data for this bin
all_frame_data = npy_data[bin_selector, :]['DM_pixel_data']
data_min = float(np.min(all_frame_data))
data_max = float(np.percentile(all_frame_data, 99))*2

with st.sidebar:
    # Create range slider for color scale
    color_range = st.slider(
        'Select color range',
        min_value=data_min,
        max_value=data_max,
        value=(data_min, data_max),
        step=0.01,
        format='%.2f'
    )

filtered_data = npy_data[bin_selector, frame_selector]['DM_pixel_data']

fig = create_plotly_heatmaps(filtered_data, color_range=color_range)
fig.update_layout(height=fig_height)

fig_histogram = create_histogram(filtered_data)


col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig)
with col2:
    st.plotly_chart(fig_histogram)
# container1.plotly_chart(fig)
# container2.plotly_chart(fig_histogram)











