from tkinter import *
from tkinter import messagebox
import tkinter as tk
import cv2
from PIL import Image, ImageTk, ImageDraw, ImageFont
import numpy as np
from datetime import datetime
import os
from qrcode_scanner import decoder
from save_data import store_data, extract_id_and_name
from dbconnection import MyDatabase

db_connection = MyDatabase('localhost', 'root', 'password', 'student_attendace_dtr', 'students_dtr')
db_connection.initialize_database()
db_connection.initialize_table()

# Define a video capture object
vid = cv2.VideoCapture(0)

# Declare the width and height in variables
width, height = 1000, 500

# Set the width and height  
vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Create a GUI app
app = Tk()
window_width = 700
window_height = 700
app.geometry(f'{window_width}x{window_height}')
app.config(bg="skyblue")

# Camera frames
camera_frame = Frame(app, width=window_width, height=window_height, bg='blue')
camera_frame.grid(row=1, column=0, padx=10, pady=5)



bottom_section_frame = Frame(app, width=300, height=100, bg='grey')
bottom_section_frame.grid(row=2, column=0, padx=10, pady=5)

# Create a label inside the camera frame to display the video
camera_label = Label(camera_frame)
camera_label.pack()  # Pack the label to fill the frame

# Global variable to store the latest frame and current name
current_frame = None
current_name = '-'  # Default name
camera_mode = None
global_id = None
global_name = None

# Flag to manage the camera loop state
loop_active = False


def add_text_to_image(frame, name, id, datetime):
    # Convert OpenCV image (BGR) to PIL image (RGB)
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_image)

    # Create a drawing context
    draw = ImageDraw.Draw(pil_image)

    # Define font and size (you can adjust the path and size as needed)
    font = ImageFont.load_default()
    
    if camera_mode == 'time_in':    
        # Define text and position
        text = f"Name: {name}\nID: {id}\nTime In: {datetime.now()}"
    else:
        text = f"Name: {name}\nID: {id}\nTime Out: {datetime.now()}"

    position = (10, 10)  # Position where text will start on the image
    
    # Get the bounding box of the text (x0, y0, x1, y1)
    text_bbox = draw.textbbox((position[0], position[1]), text, font=font)

    # Define background rectangle padding
    padding = 5

    # Define the rectangle background (adjust size based on text size)
    background_position = [
        (text_bbox[0] - padding, text_bbox[1] - padding),
        (text_bbox[2] + padding, text_bbox[3] + padding)
    ]

    # Draw the rectangle with the background color (e.g., black)
    draw.rectangle(background_position, fill=(0, 0, 0))  # Black background

    # Draw the text on the image
    draw.text(position, text, font=font, fill=(255, 255, 0))  # change the fill color here

    # Convert back to OpenCV format (RGB to BGR)
    frame_with_text = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    return frame_with_text

# Function to save the current frame
def save_info():
    global current_frame, current_name

    if current_frame is not None:

        # Ensure the 'pictures' directory exists
        if not os.path.exists('pictures'):
            os.makedirs('pictures')
        
        # Create a unique file name with a timestamp
        file_name = f'pictures/{current_name},{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
        
        #ADD A TEXT
        frame = add_text_to_image(current_frame,global_name, global_id, datetime.now())

        # Save the current frame as a PNG file
        cv2.imwrite(file_name, frame)
        print(f'Frame saved as {file_name}')
    else:
        print('No frame available to save')

# Function to open camera and display it in the label_widget on app
def open_camera():
    global current_frame, current_name, camera_mode, loop_active, global_id, global_name

    if not loop_active:
        return

    # Capture the video frame by frame
    ret, frame = vid.read()

    if ret:
        frame, barcode_data = decoder(frame)

        current_name = str(barcode_data)
        if len(current_name) > 0:
            id, name = extract_id_and_name(current_name)
            global_id = id
            global_name = name
            if camera_mode == 'time_in':
                print('time in')
                messagebox.showinfo("information", f'YOU ARE: {current_name} : {datetime.now()}') 
                # id, name = extract_id_and_name(current_name)
                db_connection.insert_data(id, name)
                save_info()
            elif camera_mode == 'time_out':
                print('time out')
                messagebox.showinfo("information", f'YOU ARE: {current_name} : {datetime.now()}') 
                # id, name = extract_id_and_name(current_name)
                db_connection.update_data(id, name)
                save_info()

        # frame_with_text = add_text_to_image(frame, name, id, datetime.now())
        # Store the latest frame globally
        current_frame = frame


        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        # Capture the latest frame and transform to image
        captured_image = Image.fromarray(opencv_image)

        # Convert captured image to PhotoImage
        photo_image = ImageTk.PhotoImage(image=captured_image)

        # Displaying photo_image in the label
        camera_label.photo_image = photo_image

        # Configure the image in the label
        camera_label.configure(image=photo_image)

    # Repeat the same process after 10 milliseconds to refresh the frame
    camera_label.after(10, open_camera)

def update_mode_label():
    # Update the text in the label to show the current mode (time_in or time_out)
    # mode_label.config(text=f"{camera_mode.upper() ?? "TIME IN": ""}")
    mode_label.config(text='TIME IN' if camera_mode.upper() == 'TIME_IN' else 'TIME OUT')



def stop_camera():
    global camera_mode, loop_active
    camera_mode = ''
    loop_active = False
    camera_label.configure(image='')
    # Optional: update the mode label to indicate camera is off
    mode_label.config(text="")

def open_time_in():
    global camera_mode, loop_active
    camera_mode = 'time_in'
    loop_active = True

    # Update mode label to "time_in"
    update_mode_label()

    open_camera()

def open_time_out():
    global camera_mode, loop_active
    camera_mode = 'time_out'
    loop_active = True

    # Update mode label to "time_out"
    update_mode_label()
    open_camera()



# Create a button to save the current frame when clicked
button_time_in = tk.Button(
    bottom_section_frame,
    text="TIME IN",
    command=open_time_in,
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
button_time_in.grid(row=1,column=0)

# Create a button to save the current frame when clicked
button_time_out = tk.Button(
    bottom_section_frame,
    text="TIME OUT",
    command=open_time_out,
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
button_time_out.grid(row=1,column=1)

# Create a button to stop the camera feed
button_stop = tk.Button(
    bottom_section_frame,
    text="STOP",
    command=stop_camera,
    activebackground="red",
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
    highlightcolor="red",
    highlightthickness=2,
    justify="center",
    overrelief="raised",
    padx=10,
    pady=5,
    width=15,
    wraplength=100
)
button_stop.grid(row=2,column=0)


# Add a label to display the current mode (time_in or time_out)
mode_label = Label(app, text="", font=("Arial", 16), bg='skyblue')
mode_label.grid(row=0, column=0, padx=10, pady=10)



# Bind the app with Escape keyboard to quit app whenever pressed
app.bind('<Escape>', lambda e: app.quit())

# Create an infinite loop for displaying the app on screen
app.mainloop()
