import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import time

class ImageGalleryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Gallery Viewer")
        self.root.geometry("800x600")
        
        # Variables for images and image index
        self.images = []
        self.current_image = None
        self.img_label = tk.Label(self.root)
        self.img_label.pack(padx=10, pady=10)
        
        # Create buttons for functionality
        self.create_buttons()
        
        # Set initial zoom and rotation values
        self.zoom_factor = 1.0
        self.rotation_angle = 0

    def create_buttons(self):
        # Browse button to select the folder
        browse_button = tk.Button(self.root, text="Browse Folder", command=self.browse_folder)
        browse_button.pack(pady=5)
        
        # Zoom buttons
        zoom_in_button = tk.Button(self.root, text="Zoom In", command=self.zoom_in)
        zoom_in_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        zoom_out_button = tk.Button(self.root, text="Zoom Out", command=self.zoom_out)
        zoom_out_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Rotate buttons
        rotate_left_button = tk.Button(self.root, text="Rotate Left", command=self.rotate_left)
        rotate_left_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        rotate_right_button = tk.Button(self.root, text="Rotate Right", command=self.rotate_right)
        rotate_right_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Slideshow button
        slideshow_button = tk.Button(self.root, text="Start Slideshow", command=self.start_slideshow)
        slideshow_button.pack(pady=5)
    
    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.load_images_from_folder(folder_path)
            self.display_image(0)
    
    def load_images_from_folder(self, folder_path):
        """Load all images from the given folder."""
        self.images = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
                       if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        if not self.images:
            messagebox.showerror("No Images", "No image files found in the folder.")
    
    def display_image(self, index):
        """Display image at the given index."""
        if not self.images:
            return
        try:
            image_path = self.images[index]
            self.current_image = Image.open(image_path)
            self.show_image()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading image: {e}")
    
    def show_image(self):
        """Show the current image in the label with applied zoom and rotation."""
        if self.current_image:
            # Apply zoom
            width, height = self.current_image.size
            new_width = int(width * self.zoom_factor)
            new_height = int(height * self.zoom_factor)
            image_resized = self.current_image.resize((new_width, new_height), Image.ANTIALIAS)
            
            # Apply rotation
            image_rotated = image_resized.rotate(self.rotation_angle)
            
            # Convert to Tkinter-compatible format
            image_tk = ImageTk.PhotoImage(image_rotated)
            
            self.img_label.config(image=image_tk)
            self.img_label.image = image_tk  # Keep a reference to avoid garbage collection
    
    def zoom_in(self):
        """Zoom in the image."""
        self.zoom_factor *= 1.1
        if self.current_image:
            self.show_image()

    def zoom_out(self):
        """Zoom out the image."""
        self.zoom_factor /= 1.1
        if self.current_image:
            self.show_image()
    
    def rotate_left(self):
        """Rotate the image to the left (counterclockwise)."""
        self.rotation_angle -= 90
        if self.current_image:
            self.show_image()
    
    def rotate_right(self):
        """Rotate the image to the right (clockwise)."""
        self.rotation_angle += 90
        if self.current_image:
            self.show_image()
    
    def start_slideshow(self):
        """Start a slideshow of images with a 2-second delay."""
        if not self.images:
            messagebox.showerror("No Images", "No images available for slideshow.")
            return
        
        self.show_slideshow(0)

    def show_slideshow(self, index):
        """Show images in slideshow mode."""
        if index >= len(self.images):
            index = 0  # Start from the first image again
        self.display_image(index)
        self.root.after(2000, self.show_slideshow, index + 1)  # Show next image after 2 seconds

# Main function to run the app
def main():
    root = tk.Tk()
    app = ImageGalleryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
