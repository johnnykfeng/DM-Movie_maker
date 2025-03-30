# %%
from modules import *

make_movie = True
process_struct_array = True
save_folder = r"V:\IQ\Animations"
data_path = r"V:\IQ\S1160-2025-Mar-12-15h26m08s-cylinder-bb"
folder_name = get_file_name(data_path)
print(folder_name)
save_path = os.path.join(save_folder, folder_name)
print(save_path)

# %%
if process_struct_array:
    
    mat_files = extract_mat_files(data_path)
    print(f"Found {len(mat_files)} .mat files")
    mat_files = sort_module_order(mat_files, source="folderpath_backslash")
    for mat_file in mat_files:
        print(mat_file)
        print(get_file_name(mat_file))
    structured_array = create_structured_array(
        mat_files, save_path=save_path
    )
     
    
# %%
if make_movie:
    # structured_array = np.load(r"structured_array_data\test.npy")

    # feature_array = np.load(r"structured_array_data\rotating_phantom_W_beads_1kHz_SDD_341_0.1Cu_13p8Al_3mA_2000_frames_0.001_resolution_20PE.npy")

    # airnorm_array = np.load(r"structured_array_data\airnorm_SDD_341_0.1Cu_13p8Al_3mA_2000_frames_0.001_resolution_20PE.npy")
    
    # normalized_array = normalize_structured_array(feature_array, airnorm_array, save_path=r"structured_array_data\normalized_rotating_phantom_W_beads_1kHz_SDD_341_0.1Cu_13p8Al_3mA_2000_frames_0.001_resolution_20PE.npy")

    normalized_array = np.load(r"structured_array_data\normalized_rotating_phantom_W_beads_1kHz_SDD_341_0.1Cu_13p8Al_3mA_2000_frames_0.001_resolution_20PE.npy")
    
    make_animation(normalized_array, 
                   frame_selector=[1000, 1500], 
                   bin_selector=6,
                   fps=30,
                   writer='ffmpeg')
    
