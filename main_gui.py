import os
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from modules import (get_file_name, 
                     extract_mat_files, 
                     sort_module_order, 
                     create_structured_array, 
                     normalize_structured_array, 
                     make_animation)

class MovieMakerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DM Movie Maker")
        self.root.geometry("800x900")
        
        # Variables
        self.data_path = tk.StringVar(value=r"C:\Users\10552\OneDrive - Redlen Technologies\Code\IMAGE QUALITY\DM-Movie-Maker\DATA\S1160-2025-Mar-12-15h26m08s-cylinder-bb\1_cylinder_0.1Cu_13p8Al_10mA_4000_frames_0.001_resolution_20PE")
        self.save_folder = tk.StringVar(value=r"C:\Users\10552\OneDrive - Redlen Technologies\Code\IMAGE QUALITY\DM-Movie-Maker\DATA\ANIMATIONS")
        self.feature_path = tk.StringVar()
        self.airnorm_path = tk.StringVar()
        self.npy_save_path = ""
        self.data_id = ""
        
        self.npy_path = tk.StringVar()
        self.movie_save_path = tk.StringVar()
        self.frame_start = tk.StringVar(value="0")
        self.frame_end = tk.StringVar(value="1000")
        self.bin_selector = tk.StringVar(value="6")
        self.fps = tk.StringVar(value="60")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Configure button styles
        style = ttk.Style()
        style.configure('Large.TButton', font=('Arial', 12, 'bold'))
        style.configure('Browse.TButton', font=('Arial', 9))
        
        # Data Path Selection
        data_frame = ttk.Frame(self.root)
        data_frame.pack(fill='x', padx=20, anchor='w')
        ttk.Label(data_frame, text="Data Path:").pack(anchor='w', pady=(5,0))
        ttk.Entry(data_frame, textvariable=self.data_path, width=100).pack(anchor='w', pady=(5,0))
        ttk.Button(data_frame, text="Browse", command=self.browse_data_path, 
                  style='Browse.TButton').pack(anchor='w', pady=5)
        
        # Save Folder Selection
        save_frame = ttk.Frame(self.root)
        save_frame.pack(fill='x', padx=20, anchor='w')
        ttk.Label(save_frame, text="Save Folder:").pack(anchor='w', pady=(5,0))
        ttk.Entry(save_frame, textvariable=self.save_folder, width=100).pack(anchor='w', pady=(5,0))
        ttk.Button(save_frame, text="Browse", command=self.browse_save_folder,
                  style='Browse.TButton').pack(anchor='w', pady=5)
        
        # Process Data Button
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill='x', padx=20, anchor='w')
        process_btn = ttk.Button(button_frame, text="Process Data", 
                               command=self.process_data,
                               style='Large.TButton')
        process_btn.pack(anchor='w', pady=10, ipady=10, ipadx=20)
        
        
        
        # Feature Array Selection
        feature_frame = ttk.Frame(self.root)
        feature_frame.pack(fill='x', padx=20, anchor='w')
        ttk.Label(feature_frame, text="Feature Array Path (.npy):").pack(anchor='w', pady=(5,0))
        ttk.Entry(feature_frame, textvariable=self.feature_path, width=100).pack(anchor='w', pady=(5,0))
        ttk.Button(feature_frame, text="Browse", command=self.browse_feature_path,
                  style='Browse.TButton').pack(anchor='w', pady=5)
        
        # Airnorm Array Selection
        airnorm_frame = ttk.Frame(self.root)
        airnorm_frame.pack(fill='x', padx=20, anchor='w')
        ttk.Label(airnorm_frame, text="AirNorm Array Path (.npy):").pack(anchor='w', pady=(5,0))
        ttk.Entry(airnorm_frame, textvariable=self.airnorm_path, width=100).pack(anchor='w', pady=(5,0))
        ttk.Button(airnorm_frame, text="Browse", command=self.browse_airnorm_path,
                  style='Browse.TButton').pack(anchor='w', pady=5)
        
        # Normalize Data
        normalize_frame = ttk.Frame(self.root)
        normalize_frame.pack(fill='x', padx=20, anchor='w')
        normalize_btn = ttk.Button(normalize_frame, text="Normalize Data", 
                               command=self.normalize_data,
                               style='Large.TButton')
        normalize_btn.pack(anchor='w', pady=10, ipady=10, ipadx=20)
        
        
        
        # NPY File Selection
        npy_frame = ttk.Frame(self.root)
        npy_frame.pack(fill='x', padx=20, anchor='w')
        ttk.Label(npy_frame, text="Struct Array Path (.npy):").pack(anchor='w', pady=(5,0))
        ttk.Entry(npy_frame, textvariable=self.npy_path, width=100).pack(anchor='w', pady=(5,0))
        ttk.Button(npy_frame, text="Browse", command=self.browse_npy_file,
                  style='Browse.TButton').pack(anchor='w', pady=5)
        
        # Animation Parameters Frame
        param_frame = ttk.LabelFrame(self.root, text="Animation Parameters")
        param_frame.pack(fill='x', padx=20, pady=10, anchor='w')
        
        # Movie Save Path
        ttk.Label(param_frame, text="Movie Save Path:").pack(anchor='w', pady=(5,0), padx=5)
        ttk.Entry(param_frame, textvariable=self.movie_save_path, width=100).pack(anchor='w', pady=(5,0))
        # ttk.Button(param_frame, text="Browse", command=self.browse_movie_save_path,
        #           style='Browse.TButton').pack(anchor='w', pady=5)
        
        # Frame Range
        ttk.Label(param_frame, text="Frame Range:").pack(anchor='w', pady=(5,0), padx=5)
        frame_range_frame = ttk.Frame(param_frame)
        frame_range_frame.pack(anchor='w', pady=5, padx=5)
        ttk.Entry(frame_range_frame, textvariable=self.frame_start, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Label(frame_range_frame, text="to").pack(side=tk.LEFT)
        ttk.Entry(frame_range_frame, textvariable=self.frame_end, width=10).pack(side=tk.LEFT, padx=5)
        
        # Bin Selector
        ttk.Label(param_frame, text="Bin Selector:").pack(anchor='w', pady=(5,0), padx=5)
        ttk.Entry(param_frame, textvariable=self.bin_selector, width=10).pack(anchor='w', pady=5, padx=5)
        
        # FPS
        ttk.Label(param_frame, text="FPS:").pack(anchor='w', pady=(5,0), padx=5)
        ttk.Entry(param_frame, textvariable=self.fps, width=10).pack(anchor='w', pady=5, padx=5)
        
        # Make Movie Button at bottom
        movie_frame = ttk.Frame(self.root)
        movie_frame.pack(fill='x', padx=20, anchor='w')
        movie_btn = ttk.Button(movie_frame, text="Make Movie",
                             command=self.process_animation,
                             style='Large.TButton')
        movie_btn.pack(anchor='w', pady=20, ipady=10, ipadx=20)
        
    def browse_data_path(self):
        folder = filedialog.askdirectory()
        if folder:
            self.data_path.set(folder)
            
    def browse_save_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.save_folder.set(folder)

    def browse_feature_path(self):
        file = filedialog.askopenfilename(filetypes=[("NumPy files", "*.npy")])
        if file:
            self.feature_path.set(file)
            
    def browse_airnorm_path(self):
        file = filedialog.askopenfilename(filetypes=[("NumPy files", "*.npy")])
        if file:
            self.airnorm_path.set(file)

    def browse_npy_file(self):
        file = filedialog.askopenfilename(filetypes=[("NumPy files", "*.npy")])
        if file:
            self.npy_path.set(file)
            
    def process_data(self):
        """Process raw .mat files into a structured numpy array.
        
        This method:
        - Takes the selected data path containing .mat files
        - Creates save folders if they don't exist
        - Extracts and sorts .mat files by module order
        - Creates a structured array from the .mat files
        - Saves the array to the specified save path
        
        Raises:
            - ValueError if data path is not selected
            - OSError if save folders cannot be created
            - Other exceptions during processing
        """
        print("Processing data")
        try:
            data_path = self.data_path.get()
            save_folder = self.save_folder.get()
            print(f"Data path: {data_path}")
            print(f"Save folder: {save_folder}")
            
            if not data_path:
                messagebox.showerror("Error", "Please select data path for processing")
                return
                
            # Check if save folder exists, create if it doesn't
            if not os.path.exists(save_folder):
                try:
                    os.makedirs(save_folder)
                    print(f"Created save folder: {save_folder}")
                except Exception as e:
                    messagebox.showerror("Error", f"Could not create save folder: {str(e)}")
                    return
            
            self.data_id = get_file_name(data_path)
            print(f"self.data_id: {self.data_id}")
            self.npy_save_path = os.path.join(save_folder, self.data_id)
            # Check if save folder exists, create if it doesn't
            if not os.path.exists(self.npy_save_path):
                try:
                    os.makedirs(self.npy_save_path)
                    print(f"Created save folder: {self.npy_save_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Could not create save folder: {str(e)}")
                    return
            
            mat_files = extract_mat_files(data_path)
            print(f"Found {len(mat_files)} .mat files")
            mat_files = sort_module_order(mat_files, source="folderpath_backslash")
                
            structured_array = create_structured_array(
                mat_files, save_path=self.npy_save_path
            )
            messagebox.showinfo("Success", "Data processing completed successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error during data processing: {str(e)}")

    def normalize_data(self):
        """Normalize X-ray data using air normalization.
        
        This method:
        - Takes the selected feature array path and airnorm array path
        - Loads the arrays
        - Normalizes the feature array using the airnorm array
        - Saves the normalized array to the specified save path
        
        Raises:
            - ValueError if feature or airnorm array path is not selected
            - OSError if save folders cannot be created
            - Other exceptions during processing
        """
        try:
            print("Normalizing data")
            feature_path = self.feature_path.get()
            airnorm_path = self.airnorm_path.get()
            feature_array = np.load(feature_path)
            airnorm_array = np.load(airnorm_path)
            save_path = feature_path.replace(".npy", "_normalized.npy")
            print(f"Feature path: {feature_path}")
            print(f"Airnorm path: {airnorm_path}")
            print(f"Save path: {save_path}")
            normalize_structured_array(feature_array, airnorm_array, save_path=save_path)
            messagebox.showinfo("Success", "Data normalization completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error during data normalization: {str(e)}")
        
    def process_animation(self):
        """Create an MP4 animation from a structured numpy array.
        
        This method:
        - Takes the selected .npy file path and save folder
        - Loads the array
        - Creates an MP4 animation from the array
        - Saves the animation to the specified save path
        
        Raises:
            - ValueError if save folder is not selected
            - OSError if save folders cannot be created
            - Other exceptions during processing
        """
        try:
            print("Processing animation")
            save_folder = self.save_folder.get()
            npy_path = self.npy_path.get()

            print(f"Npy path: {npy_path}")
            
            # Ask user for confirmation before proceeding
            if not messagebox.askyesno("Confirm", "Ready to create animation. Continue?"):
                return
                
            if not os.path.exists(npy_path):
                messagebox.showerror("Error", "Selected .npy file does not exist")
                return
            
            # Check if file has .npy extension
            if not npy_path.endswith('.npy'):
                messagebox.showerror("Error", "Selected file must have .npy extension")
                return
                
            if not os.path.exists(save_folder):
                try:
                    os.makedirs(save_folder)
                    print(f"Created save folder: {save_folder}")
                except Exception as e:
                    messagebox.showerror("Error", f"Could not create save folder: {str(e)}")
                    return
                    
            structured_array = np.load(npy_path)
            movie_name = get_file_name(npy_path, remove_extension=True)
            if self.movie_save_path.get():
                movie_path = self.movie_save_path.get()
            else:
                movie_path = os.path.join(save_folder, f"{movie_name}.mp4")
            
            make_animation(structured_array,
                         frame_selector=[int(self.frame_start.get()), int(self.frame_end.get())],
                         bin_selector=int(self.bin_selector.get()),
                         fps=int(self.fps.get()),
                         writer='ffmpeg',
                         save_path=movie_path)
                         
            messagebox.showinfo("Success", "Movie creation completed successfully!")
            return f"Successfully created movie at {movie_path}!"
            
        except Exception as e:
            messagebox.showerror("Error", f"Error during movie creation: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieMakerGUI(root)
    root.mainloop() 