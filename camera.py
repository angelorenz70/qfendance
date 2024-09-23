from tkinter import *
from tkinter import messagebox
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import numpy as np
from datetime import datetime
from qrcode_scanner import decoder
from save_data import store_data, extract_id_and_name
from dbconnection import MyDatabase
from tools import Button, SaveImage
from face_detection import FaceDetection

db_connection = MyDatabase('localhost', 'root', 'password', 'student_attendace_dtr', 'students_dtr', 'student_users', 'under_time')
db_connection.initialize_database()
db_connection.initialize_tables()

#import model
face_detection = FaceDetection()

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

# Function to open camera and display it in the label_widget on app
def open_camera():
    global current_frame, current_name, camera_mode, loop_active, global_id, global_name

    if not loop_active:
        return

    # Capture the video frame by frame
    ret, frame = vid.read()

    if ret:
        face_detected = face_detection.detect(frame)
        if face_detected:
            #for face
            # detected = face_detection.detect(frame)
            frame, barcode_data = decoder(frame)

            # frame_with_text = add_text_to_image(frame, name, id, datetime.now())
            # Store the latest frame globally
            current_frame = frame
            current_name = str(barcode_data)

            
            if len(current_name) > 0:
                print('ENTER QRCODE AND FACE DETECTED')
                id, name, graduated= extract_id_and_name(current_name)
                print(id, name, graduated)
                
                global_id = id
                global_name = name
                if camera_mode == 'time_in':
                    messagebox.showinfo("information", f'YOU ARE: {current_name} : {datetime.now()}') 
                    # id, name = extract_id_and_name(current_name)
                    db_connection.insert_data(id, name, graduated, camera_mode)
                    SaveImage().save(current_frame, current_name, global_id, global_name, camera_mode)
                elif camera_mode == 'time_out':
                    messagebox.showinfo("information", f'YOU ARE: {current_name} : {datetime.now()}') 
                    # id, name = extract_id_and_name(current_name)
                    db_connection.update_data(id, name,graduated, camera_mode)
                    SaveImage().save(current_frame, current_name, global_id, global_name, camera_mode)
                    db_connection.calculate_undertime(global_id, datetime.now().date())

                elif camera_mode == 'break_out':
                    messagebox.showinfo("information", f'YOU ARE: {current_name} : {datetime.now()}') 
                    # id, name = extract_id_and_name(current_name)
                    db_connection.update_data(id, name,graduated, camera_mode)
                    SaveImage().save(current_frame, current_name, global_id, global_name, camera_mode)

                elif camera_mode == 'break_in':
                    messagebox.showinfo("information", f'YOU ARE: {current_name} : {datetime.now()}') 
                    # id, name = extract_id_and_name(current_name)
                    db_connection.update_data(id, name,graduated, camera_mode)
                    SaveImage().save(current_frame, current_name, global_id, global_name, camera_mode)


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
    if camera_mode.upper() == 'TIME_IN':
        mode_label.config(text='TIME IN')
    elif camera_mode.upper() == 'TIME_OUT':
        mode_label.config(text='TIME OUT')
    elif camera_mode.upper() == 'BREAK_OUT':
        mode_label.config(text='BREAK OUT')
    else:
        mode_label.config(text='BREAK IN')

    # mode_label.config(text='TIME IN' if camera_mode.upper() == 'TIME_IN' else 'TIME OUT')



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

def open_break_out():
    global camera_mode, loop_active
    camera_mode = 'break_out'
    loop_active = True
    # Update mode label to "time_out"
    update_mode_label()
    open_camera()

def open_break_in():
    global camera_mode, loop_active
    camera_mode = 'break_in'
    loop_active = True
    # Update mode label to "time_out"
    update_mode_label()
    open_camera()


# Create a button for time in
button_time_in = Button(bottom_section_frame, "TIME IN", open_time_in).button
button_time_in.grid(row=1,column=0)


# Create a button for time out
button_time_out = Button(bottom_section_frame, "BREAK OUT", open_break_out).button
button_time_out.grid(row=1,column=1)

# Create a button for time out
button_time_out = Button(bottom_section_frame, "BREAK IN", open_break_in).button
button_time_out.grid(row=1,column=2)

# Create a button for time out
button_time_out = Button(bottom_section_frame, "TIME OUT", open_time_out).button
button_time_out.grid(row=2,column=0)

# Create a button for reset or stop when there is freeze frame
button_stop = Button(bottom_section_frame, "STOP", stop_camera).button
button_stop.grid(row=2,column=1)

# Add a label to display the current mode (time_in or time_out)
mode_label = Label(app, text="", font=("Arial", 16), bg='skyblue')
mode_label.grid(row=0, column=0, padx=10, pady=10)



# Bind the app with Escape keyboard to quit app whenever pressed
app.bind('<Escape>', lambda e: app.quit())

# Create an infinite loop for displaying the app on screen
app.mainloop()
