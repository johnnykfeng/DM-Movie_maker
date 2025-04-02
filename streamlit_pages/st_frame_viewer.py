import streamlit as st
import numpy as np
import plotly.express as px
from modules import create_plotly_heatmaps, create_histogram
import pandas as pd
import time

st.set_page_config(layout="wide")

st.title("DM Frame Viewer")
with st.sidebar:
    file_source = st.radio("File source", options=["Local", "File Uploader"], index=1)
    if file_source == "Local":
        npy_path = st.text_input("Enter the path to the .npy file", value=r"C:\Users\10552\OneDrive - Redlen Technologies\Code\IMAGE QUALITY\DM-Movie-Maker\TEST_DATA\1_lower-beads_10.0mA_10_frames_0.025_resolution\struct_array_normalized.npy")
        npy_data = np.load(npy_path)
    else:
        npy_path = st.file_uploader("Upload a .npy file", type="npy")
        if npy_path is not None:
            npy_data = np.load(npy_path)
        else:
            st.warning("Please upload a .npy file")
            st.stop()

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

    fig_height = st.slider("Select the height of the figure", min_value=100, max_value=1000, value=600)

    st.subheader("Histogram settings")
    frame_step = st.number_input("Frame step", value=1, min_value=1, max_value=n_total_frames-1)

    # Create a slider for frame selection
    frame_selector = st.number_input("Frame selector", 
                                     min_value=0, 
                                     max_value=n_total_frames-1, 
                                     value=0, step=frame_step)
        
    

# Get min and max values across all data for this bin
all_frame_data = npy_data[bin_selector, :]['DM_pixel_data']
data_min = float(np.min(all_frame_data))
data_max = float(np.percentile(all_frame_data, 99))*2
# data_max = 60e3
st.write(f"**Data min:** {data_min}")
st.write(f"**Data max:** {data_max}")

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

with st.expander("**Visualization settings**"):
    cols = st.columns(5)
    with cols[0]:
        show_histogram = st.checkbox("Histogram", value=True)
    with cols[1]:
        show_column_avg = st.checkbox("Column-wise average", value=False)
    with cols[2]:
        show_row_avg = st.checkbox("Row-wise average", value=False)
    with cols[3]:
        show_column_line = st.checkbox("Column-wise line", value=False)
    with cols[4]:
        show_row_line = st.checkbox("Row-wise line", value=False)
    
    cols_b = st.columns(5)
    with cols_b[0]:
        max_y_value = st.number_input("Max y value", value=500, min_value=100, max_value=1000)
        max_x_value = st.number_input("Max x value", value=data_max, min_value=0.0)
    with cols_b[3]:
        column_selector = st.number_input("Column (x-index) selector", 
                                        min_value=0, 
                                        max_value=71, 
                                        value=31, step=1)
    with cols_b[4]:
        row_selector = st.number_input("Row (y-index) selector", 
                                        min_value=0, 
                                        max_value=191, 
                                        value=43, step=1) 

st.write(f"**Selected bin:** {bin_selector}")
st.write(f"**Selected frame:** {frame_selector}")

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig)
with col2:
    if show_histogram:
        fig_histogram = create_histogram(filtered_data)
        fig_histogram.update_layout(yaxis_range=[np.log10(0.5), np.log10(max_y_value)], xaxis_range=[0, max_x_value])
        st.plotly_chart(fig_histogram)


    if show_column_avg:
        # Calculate column-wise average
        column_averages = np.mean(filtered_data, axis=0)

        # Create line plot of column averages
        fig_column_avg = px.line(column_averages, 
                                labels={'index': 'Column Number (x)', 'value': 'Average Value'},
                                title='Column-wise Average',
                                markers=True)


        # Customize marker appearance (optional)
        fig_column_avg.update_traces(marker=dict(size=4),  # Change marker size
                                line=dict(width=1))      # Change line width

        st.plotly_chart(fig_column_avg)

    if show_row_avg:
        # Calculate row-wise average
        row_averages = np.mean(filtered_data, axis=1)

        # Create line plot of row averages
        fig_row_avg = px.line(row_averages,
                            labels={'index': 'Row Number (y)', 'value': 'Average Value'}, 
                            title='Row-wise Average',
                            markers=True)
        fig_row_avg.update_traces(marker=dict(size=4),  # Change marker size
                                line=dict(width=1))      # Change line width

        st.plotly_chart(fig_row_avg)
        
    
    if show_column_line:
        fig_column_avg = px.line(filtered_data[:, column_selector], 
                                labels={'index': 'x-index', 'value': 'Pixel Value'},
                                title=f'Column x={column_selector}',
                                markers=True)
        fig_column_avg.update_traces(marker=dict(size=4),  # Change marker size
                                line=dict(width=1))      # Change line width
        fig_column_avg.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
        st.plotly_chart(fig_column_avg)
    
    if show_row_line:
        fig_row_avg = px.line(filtered_data[row_selector, :], 
                            labels={'index': 'y-index', 'value': 'Pixel Value'},
                            title=f'Row y={row_selector}',
                            markers=True)
        fig_row_avg.update_traces(marker=dict(size=4),  # Change marker size
                                line=dict(width=1))      # Change line width
        fig_row_avg.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
        st.plotly_chart(fig_row_avg)
















