import cv2
import face_recognition
import numpy as np
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk

# Initialize global variables
known_face_encoding = None
verify_face_encoding = None

def load_faces():
    """Load images and compare faces."""
    global known_face_encoding, verify_face_encoding
    
    # Open file dialog to select known image and image to verify
    known_image_path = filedialog.askopenfilename(title="Select Known Image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    verify_image_path = filedialog.askopenfilename(title="Select Image to Verify", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])

    try:
        # Load the known image
        known_image = face_recognition.load_image_file(known_image_path)
        known_face_encoding = face_recognition.face_encodings(known_image)[0]
        
        # Load the image to verify
        verify_image = face_recognition.load_image_file(verify_image_path)
        verify_face_encoding = face_recognition.face_encodings(verify_image)[0]
        
        # Compare the faces
        result = face_recognition.compare_faces([known_face_encoding], verify_face_encoding)
        
        # Display images and comparison result
        display_images(known_image, verify_image, result[0])

    except IndexError:
        messagebox.showerror("Error", "Could not detect faces in one or both images.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not load images: {e}")

def display_images(known_image, verify_image, match_result):
    """Display both the known image and the image to verify."""
    
    # Convert images to RGB
    known_image_rgb = cv2.cvtColor(known_image, cv2.COLOR_BGR2RGB)
    verify_image_rgb = cv2.cvtColor(verify_image, cv2.COLOR_BGR2RGB)

    # Resize images for display
    known_image_pil = Image.fromarray(known_image_rgb)
    verify_image_pil = Image.fromarray(verify_image_rgb)
    
    known_image_pil.thumbnail((250, 250))
    verify_image_pil.thumbnail((250, 250))
    
    # Convert to PhotoImage
    known_image_tk = ImageTk.PhotoImage(known_image_pil)
    verify_image_tk = ImageTk.PhotoImage(verify_image_pil)
    
    # Display known image
    known_label.config(image=known_image_tk)
    known_label.image = known_image_tk  # Keep a reference to avoid garbage collection
    
    # Display verify image
    verify_label.config(image=verify_image_tk)
    verify_label.image = verify_image_tk  # Keep a reference to avoid garbage collection
    
    # Display match result
    if match_result:
        result_label.config(text="Result: Faces Match!", fg="green")
    else:
        result_label.config(text="Result: Faces Do Not Match!", fg="red")

# Set up the GUI
root = tk.Tk()
root.title("Facial Recognition Image Comparison")

# Set window size
root.geometry("600x400")

# Create image labels
known_label = tk.Label(root, text="Known Image")
known_label.grid(row=0, column=0, padx=20, pady=20)

verify_label = tk.Label(root, text="Verify Image")
verify_label.grid(row=0, column=1, padx=20, pady=20)

# Result label
result_label = tk.Label(root, text="Result: ", font=("Arial", 16))
result_label.grid(row=1, column=0, columnspan=2, pady=20)

# Create buttons
load_faces_button = tk.Button(root, text="Load and Compare Faces", command=load_faces, font=("Arial", 14), bg="lightblue")
load_faces_button.grid(row=2, column=0, columnspan=2, pady=10)

# Start the Tkinter event loop
root.mainloop()
