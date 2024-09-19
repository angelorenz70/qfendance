from tkinter import *
from tkinter import messagebox
import tkinter as tk
import cv2
from PIL import Image, ImageTk
from datetime import datetime
from set_all_face import set_faces
from face_recognize import recognize_face
import os
from qrcode_scanner import decoder
from save_data import store_data


# Initialize the faces
faces = set_faces()

# Define a video capture object
vid = cv2.VideoCapture(0)

# Declare the width and height in variables
width, height = 1000, 500

# Set the width and height  
vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Create a GUI app
app = Tk()
window_width = 1000
window_height = 900
app.geometry(f'{window_width}x{window_height}')
app.config(bg="skyblue")


# declare a variable used for input
name_var=tk.StringVar()

# Create left and right frames
sidebar_frame = Frame(app, width=400, height=850, bg='grey')
sidebar_frame.grid(row=1, column=0, padx=10, pady=5)

input_label = Label()

# Camera frames
camera_frame = Frame(app, width=1150, height=850, bg='blue')
camera_frame.grid(row=1, column=1, padx=10, pady=5)

# Create a label inside the camera frame to display the video
camera_label = Label(camera_frame)
camera_label.pack()  # Pack the label to fill the frame

# Global variable to store the latest frame and current name
current_frame = None
current_name = '-'  # Default name

# Function to save the current frame
def save_info():
    print('save info')
    global current_frame, current_name
    if current_frame is not None:
        # Ensure the 'pictures' directory exists
        if not os.path.exists('pictures'):
            os.makedirs('pictures')
        
        # Create a unique file name with a timestamp
        file_name = f'pictures/{current_name},{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
        
        # Save the current frame as a PNG file
        cv2.imwrite(file_name, current_frame)
        print(f'Frame saved as {file_name}')
    else:
        print('No frame available to save')

# Function to open camera and display it in the label_widget on app
def open_camera():
    global current_frame, current_name

    # Capture the video frame by frame
    ret, frame = vid.read()

    if ret:
        frame, name = recognize_face(frame, faces)
        current_name = name

        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        # Capture the latest frame and transform to image
        captured_image = Image.fromarray(opencv_image)

        # Convert captured image to PhotoImage
        photo_image = ImageTk.PhotoImage(image=captured_image)

        # Displaying photo_image in the label
        camera_label.photo_image = photo_image 

        # Configure the image in the label
        camera_label.configure(image=photo_image)

        # Store the latest frame globally
        current_frame = frame

    # Repeat the same process after 10 milliseconds to refresh the frame
    camera_label.after(1, open_camera)

# Start the camera feed
open_camera()

# Create a button to save the current frame when clicked
button = tk.Button(
    sidebar_frame,
    text="SAVE FRAME",
    command=save_info,  # No need for lambda here as we are not passing arguments
    activebackground="blue",
    activeforeground="white",
    anchor="center",
    bd=3,
    bg="lightgray",
    cursor="hand2",
    disabledforeground="gray",
    fg="black",
    font=("Arial", 12),
    height=2,
    highlightbackground="black",
    highlightcolor="green",
    highlightthickness=2,
    justify="center",
    overrelief="raised",
    padx=10,
    pady=5,
    width=15,
    wraplength=100
)
# button.pack()
button.grid(row=0,column=0)

# creating a label for 
# name using widget Label
name_label = tk.Label(sidebar_frame, text = 'STUDENT NAME', font=('calibre',10, 'bold'), pady=5)
name_label.grid(row=1,column=0)
 
# creating a entry for input
# name using widget Entry
name_entry = tk.Entry(sidebar_frame,textvariable = name_var, font=('calibre',10,'normal'))
name_entry.grid(row=2,column=0)

def submit():
    name=name_var.get()
    print("The name is : " + name)    
    name_var.set("")

    # Create a unique file name with a timestamp
    file_name = f'images/{name}, {datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
    
    # Save the current frame as a PNG file
    cv2.imwrite(file_name, current_frame)

sub_btn=tk.Button(sidebar_frame,text = 'Submit', command = submit)
sub_btn.grid(row=3, column=0)

# Bind the app with Escape keyboard to quit app whenever pressed
app.bind('<Escape>', lambda e: app.quit())

# Create an infinite loop for displaying the app on screen
app.mainloop()
