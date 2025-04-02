import streamlit as st
import numpy as np
import plotly.express as px
from modules import create_plotly_heatmaps, create_histogram
import pandas as pd
import time
from config import BIN_LABELS

st.set_page_config(layout="wide")

st.title("DM Frame-by-Frame Animation")
with st.sidebar:
    npy_path = st.text_input("Enter the path to the .npy file", value=r"DATA\ANIMATIONS\1_cylinder_0.1Cu_13p8Al_10mA_4000_frames_0.001_resolution_20PE_normalized.npy")
    frame_time = st.number_input("Frame time (ms)", value=10, min_value=5, max_value=1000)
    full_speed = st.checkbox("Full speed", value=False)


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
        format_func=lambda x: f'Bin {x}',
        index=6
    )

    start_frame = st.number_input("Start frame", value=0, min_value=0, max_value=n_total_frames-1)
    end_frame = st.number_input("End frame", value=n_total_frames-1, min_value=0, max_value=n_total_frames-1)
    step_frame = st.number_input("Step frame", value=1, min_value=1, max_value=n_total_frames-1)

    fig_height = st.slider("Select the height of the figure", min_value=100, max_value=1000, value=600)
    

with st.expander("**Visualization settings**"):
    control_cols = st.columns(5)
    with control_cols[0]:
        histogram_toggle = st.checkbox("Histogram", value=False)
    with control_cols[1]:
        column_avg_toggle = st.checkbox("Column-wise average", value=False)
    with control_cols[2]:
        row_avg_toggle = st.checkbox("Row-wise average", value=False)
    with control_cols[3]:
        column_line_toggle = st.checkbox("Column-wise line", value=False)
    with control_cols[4]:
        row_line_toggle = st.checkbox("Row-wise line", value=False)

    control_cols_b = st.columns(5)
    with control_cols_b[0]:
        # st.write("**Histogram settings**")
        max_y_value = st.number_input("Max y value", value=500, min_value=100, max_value=1000)
        max_x_value = st.number_input("Max x value", value=2.0, min_value=1.0, max_value=30.0)
        
    with control_cols_b[3]:
        column_selector = st.number_input("Column (x-index) selector", 
                                        min_value=0, 
                                        max_value=71, 
                                        value=31, step=1,
                                        key=f"column_selector")
    with control_cols_b[4]:
        row_selector = st.number_input("Row (y-index) selector", 
                                        min_value=0, 
                                        max_value=191, 
                                        value=43, step=1,
                                        key=f"row_selector")

st.write(f"**Bin: {bin_selector} ({BIN_LABELS[bin_selector]})**")
control_container = st.container()
frame_num_container = st.empty()

col1, col2 = st.columns(2)
with col1:
    container1 = st.empty()
with col2:
    container2 = st.empty()


# Get min and max values across all data for this bin
all_frame_data = npy_data[bin_selector, :]['DM_pixel_data']
data_min = float(np.min(all_frame_data))
data_max = float(np.percentile(all_frame_data, 99))*2

with control_container:
    # Add start/stop control
    start_stop_col1, start_stop_col2 = st.columns(2)
    with start_stop_col1:
        play_animation = st.toggle("Play animation", value=False)
    with start_stop_col2:
        capture_frame = st.button("Capture frame")

# Initialize animation state if not exists
if 'animation_running' not in st.session_state:
    st.session_state.animation_running = False
if 'frame_number' not in st.session_state:
    st.session_state.frame_number = 0

# Update animation state based on button clicks    
if play_animation:
    st.session_state.animation_running = True
elif not play_animation:
    st.session_state.animation_running = False

if capture_frame:
    st.session_state.animation_running = False

# Only run animation loop if animation is running
if not st.session_state.animation_running:
    # Show single frame when stopped
    filtered_data = npy_data[bin_selector, st.session_state.frame_number]['DM_pixel_data']
    fig = create_plotly_heatmaps(filtered_data, color_range=[data_min, data_max])
    fig.update_layout(height=fig_height)
    container1.plotly_chart(fig)
    frame_num_container.write(f"Frame {st.session_state.frame_number}")
    with container2:
        if histogram_toggle:
            fig_histogram = create_histogram(filtered_data, max_y_value=max_y_value, max_x_value=max_x_value)
            st.plotly_chart(fig_histogram)
        if column_avg_toggle:
            column_averages = np.mean(filtered_data, axis=0)
            fig_column_avg = px.line(column_averages, 
                                    labels={'index': 'Column Number (x)', 'value': 'Average Value'},
                                    title='Column-wise Average',
                                    markers=True)
            st.plotly_chart(fig_column_avg)
        if row_avg_toggle:
            row_averages = np.mean(filtered_data, axis=1)
            fig_row_avg = px.line(row_averages,
                                labels={'index': 'Row Number (y)', 'value': 'Average Value'}, 
                                title='Row-wise Average',
                                markers=True)
            st.plotly_chart(fig_row_avg)

else:
    for frame in range(start_frame, end_frame, step_frame):
        st.session_state.frame_number = frame
        frame_num_container.write(f"Frame {st.session_state.frame_number}")
        if not full_speed:
            time.sleep(frame_time/1000)

        filtered_data = npy_data[bin_selector, frame]['DM_pixel_data']

        fig = create_plotly_heatmaps(filtered_data, color_range=[data_min, data_max])
        fig.update_layout(height=fig_height)
        container1.plotly_chart(fig)

        with container2:
            if histogram_toggle:
                fig_histogram = create_histogram(filtered_data)
                fig_histogram.update_layout(yaxis_range=[np.log10(0.2), np.log10(max_y_value)], xaxis_range=[0, max_x_value])
                st.plotly_chart(fig_histogram)
                
            if column_avg_toggle:
                column_averages = np.mean(filtered_data, axis=0)
                fig_column_avg = px.line(column_averages, 
                                        labels={'index': 'Column Number (x)', 'value': 'Average Value'},
                                        title='Column-wise Average',
                                        markers=True)
                st.plotly_chart(fig_column_avg)
                
            if row_avg_toggle:
                row_averages = np.mean(filtered_data, axis=1)
                fig_row_avg = px.line(row_averages,
                                    labels={'index': 'Row Number (y)', 'value': 'Average Value'}, 
                                    title='Row-wise Average',
                                    markers=True)
                st.plotly_chart(fig_row_avg)
                
            if column_line_toggle:
                fig_column_line = px.line(filtered_data[:, column_selector], 
                                labels={'index': 'Frame Number', 'value': 'Pixel Value'},
                                title=f'Column {column_selector} Average')
                st.plotly_chart(fig_column_line)
            
            if row_line_toggle:
                fig_row_line = px.line(filtered_data[row_selector, :], 
                            labels={'index': 'Frame Number', 'value': 'Pixel Value'},
                            title=f'Row {row_selector} Average')
                st.plotly_chart(fig_row_line)










