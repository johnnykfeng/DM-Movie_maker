import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import scipy.io
import os
import time
from config import MM_ORDER

def sort_module_order(
    files: list, source: str = "streamlit_uploader", module_order=MM_ORDER
):
    if source == "streamlit_uploader":
        files.sort(
            key=lambda x: module_order.index(x.name.split("-")[0])
            if x.name.split("-")[0] in module_order
            else ValueError("File not in module order")
        )
    elif source == "folderpath_backslash":
        files.sort(
            key=lambda x: module_order.index(x.split("\\")[-1].split("-")[0])
            if x.split("\\")[-1].split("-")[0] in module_order
            else ValueError("File not in module order")
        )
    elif source == "folderpath_forward_slash":
        files.sort(
            key=lambda x: module_order.index(x.split("/")[-1].split("-")[0])
            if x.split("/")[-1].split("-")[0] in module_order
            else ValueError("File not in module order")
        )
    else:
        raise ValueError("Invalid 'source' argument")
    return files

def get_file_name(file_path, remove_extension=False):
    if remove_extension:
        file_name = os.path.basename(file_path)
        extension = os.path.splitext(file_name)[1]
        file_name = file_name.replace(extension, "")
        return file_name
    else:
        return os.path.basename(file_path)


def extract_mat_files(folder_path):
    mat_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".mat"):
                mat_files.append(os.path.join(root, file))
    return mat_files


def create_structured_array(mat_files: list, save_path: str = None, verbose: bool = False):
    """
    Create a structured array from the data in the data_path.
    """
    start_time = time.time()
    # mat_files = extract_mat_files(data_path)
    # mat_files = sort_module_order(mat_files, source=data_source)
    all_cc_data = []
    for m, mat_file in enumerate(mat_files):
        file_name = get_file_name(mat_file).replace(".mat", "")
        mat_file = scipy.io.loadmat(mat_file)
        cc_data = mat_file["cc_struct"]["data"][0][0][0][0][0]
        all_cc_data.append({file_name: cc_data})

        if verbose:
            print(f"Mat file: {file_name}")
        if m == 0:
            num_sample_frames = cc_data.shape[2]
            num_bins = cc_data.shape[1]
            print(f"{num_sample_frames = }")
            print(f"{num_bins = }")

    # Initialize structured array
    structured_dtype = np.dtype(
        [
            ("bin_id", "i4"),
            ("frame_number", "i4"),
            ("DM_pixel_data", "f4", (192, 72)),
        ]
    )
    structured_array = np.empty((num_bins, num_sample_frames), dtype=structured_dtype)

    for bin_idx in range(num_bins):
        for frame_idx in range(num_sample_frames):
            # print(f"bin_idx: {bin_idx}, frame_idx: {frame_idx}")
            count_maps_A0 = []
            count_maps_A1 = []
            # Loop through all modules' data
            for cc_data_dict in all_cc_data:
                for file_name, cc_data in cc_data_dict.items():
                    mm_order = file_name.split("-")[1]
                    # Get count map for this specific module
                    count_map = cc_data[0, bin_idx, frame_idx, :, :]

                    if mm_order == "A0":
                        count_map = np.flip(count_map, axis=0)
                        count_map = np.flip(count_map, axis=1)
                        count_maps_A0.append(count_map)
                    elif mm_order == "A1":
                        count_maps_A1.append(count_map)
                    else:
                        raise ValueError(f"Invalid mm_order: {mm_order}")

            count_maps_A0_comb = np.concatenate(count_maps_A0, axis=0)
            count_maps_A1_comb = np.concatenate(count_maps_A1, axis=0)
            DM_count_map = np.concatenate(
                [count_maps_A0_comb, count_maps_A1_comb], axis=1
            )
            # print(DM_count_map.shape)
            structured_array[bin_idx, frame_idx] = (bin_idx, frame_idx, DM_count_map)

    if save_path:
        np.save(save_path, structured_array)
        print(f"Saved structured array to {save_path}")
    end_time = time.time()
    print(f"Data processing completed in {round(end_time - start_time, 1)} seconds")
    return structured_array
   
def normalize_structured_array(feature_array, airnorm_array, save_path: str = None):
    n_bins = feature_array.shape[0]
    n_total_frames = feature_array.shape[1]
    structured_dtype = np.dtype([("bin_id", "i4"),
                                ("frame_number", "i4"),
                                ("DM_pixel_data", "f4", (192, 72))])
    normalized_array = np.empty((n_bins, n_total_frames), dtype=structured_dtype)
    for bin_idx in range(n_bins):
        # average the airnorm array per bin
        airnorm_averaged_per_bin = np.mean(airnorm_array[bin_idx, :]['DM_pixel_data'], axis=0)
        for frame_idx in range(n_total_frames):   
            feature_pixel_data = feature_array[bin_idx, frame_idx]['DM_pixel_data']
            # set pixels with zero airnorm to 1
            airnorm_averaged_per_bin[airnorm_averaged_per_bin == 0] = 1
            # normalize the feature pixel data by pixel wise or element wise division
            normalized_pixel_data = np.divide(feature_pixel_data, airnorm_averaged_per_bin)
            # replace nan with 0
            normalized_pixel_data = np.nan_to_num(normalized_pixel_data)
            normalized_array[bin_idx, frame_idx] = (bin_idx, frame_idx, normalized_pixel_data)
            
    if save_path:
        np.save(save_path, normalized_array)
        print(f"Saved normalized structured array to {save_path}")
    return normalized_array

   
def make_animation(structured_array, 
                   bin_selector=6,
                   frame_selector=[0, 200], 
                   fps=30,
                   writer='html', 
                   save_path=None):
    n_bins = structured_array.shape[0]
    n_total_frames = structured_array.shape[1]
    print(f"{n_bins = }")
    print(f"{n_total_frames = }")
    
    if frame_selector == None:
        frame_selector = [0, n_total_frames]
    elif isinstance(frame_selector, list):
        if frame_selector[1] > n_total_frames:
            frame_selector[1] = n_total_frames
    else:
        raise ValueError(f"Invalid frame_selector: {frame_selector}")

    frames_to_animate = np.arange(frame_selector[0], frame_selector[1])
    # loaded_structured_array = structured_array
    frame_interval = 1000 / fps
    print(f"{frame_interval = }")
    
    start_time = time.time()
    # Create figure and axis for animation
    fig, ax = plt.subplots(figsize=(5.2, 12))

    bin_selector = 6
    # Calculate global color range using percentiles across all frames
    all_data = structured_array[bin_selector, frames_to_animate]['DM_pixel_data']
    global_color_min, global_color_max = np.percentile(all_data, [1, 98])
    print(f"{global_color_min = }")
    print(f"{global_color_max = }")
    # Initialize the plot with first frame
    im = ax.imshow(structured_array[bin_selector, 0]['DM_pixel_data'],
                cmap='viridis',
                vmin=global_color_min,
                vmax=global_color_max,
                aspect='auto')

    # Add colorbar
    plt.colorbar(im, label='Counts')

    # Add labels
    ax.set_xlabel('Pixel Column')
    ax.set_ylabel('Pixel Row')

    # Animation update function
    def update(frame):
        # Update image data
        im.set_array(structured_array[bin_selector, frame]['DM_pixel_data'])
        # Update title
        ax.set_title(f'Bin {bin_selector}, Frame {frame}')
        return [im]

    # Create animation
    anim = animation.FuncAnimation(fig, update, frames=frames_to_animate, 
                                interval=frame_interval, blit=True)

    # Save animation
    if save_path:
        animation_name = save_path
        anim.save(animation_name, writer=writer)
    else:
        save_name = f'test_animation_bin-{bin_selector}_frames-{frame_selector[0]}to{frame_selector[1]}'
        if writer == 'html':
            animation_name = f'{save_name}.html'
        elif writer == 'ffmpeg':
            animation_name = f'{save_name}.mp4'
        elif writer == 'pillow':
            animation_name = f'{save_name}.gif'
        else:
            raise ValueError(f"Invalid writer: {writer}")
        anim.save(animation_name, writer=writer)

    plt.close()
    print(f"Animation saved as '{animation_name}'")
    end_time = time.time()
    print(f"Animation saved in {round(end_time - start_time, 1)} seconds")
