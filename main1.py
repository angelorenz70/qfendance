from tkinter import *
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
from datetime import datetime
import os

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1000x900')
        self.root.config(bg="skyblue")
        
        # Define buttons and labels
        self.time_in_button = Button(root, text="Time In", command=self.time_in)
        self.time_in_button.pack(pady=20)
        
        self.time_out_button = Button(root, text="Time Out", command=self.time_out)
        self.time_out_button.pack(pady=20)

        # Define the labels to display the QR code scan result
        self.info_label = Label(root, text="")
        self.info_label.pack(pady=20)

        # Initialize camera
        self.vid = cv2.VideoCapture(0)
        self.camera_frame = Frame(root, width=800, height=600, bg='blue')
        self.camera_frame.pack(pady=20)
        self.camera_label = Label(self.camera_frame)
        self.camera_label.pack()

        # Initialize time_in and time_out
        self.time_in_data = None
        self.time_out_data = None

        # Start the camera feed
        self.open_camera()

    def open_camera(self):
        ret, frame = self.vid.read()
        if ret:
            # Convert the frame to RGB format
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(rgb_frame)
            photo_image = ImageTk.PhotoImage(image=image)
            self.camera_label.photo_image = photo_image
            self.camera_label.configure(image=photo_image)

            # Check for QR code and update time_in_data or time_out_data accordingly
            # Here you can integrate your QR code scanning logic
            # For example:
            # barcode_data = decoder(frame)  # Implement decoder to scan QR code
            # if barcode_data:
            #     self.info_label.config(text=f"Scanned QR Code: {barcode_data}")

        self.camera_label.after(10, self.open_camera)

    def time_in(self):
        if self.time_in_data is None:
            self.time_in_data = datetime.now()
            self.info_label.config(text=f"Time In: {self.time_in_data}")
            # Here you can add logic to wait for QR code scan
            messagebox.showinfo("Information", "Scan the QR Code for Time In")

    def time_out(self):
        if self.time_in_data is not None:
            self.time_out_data = datetime.now()
            self.info_label.config(text=f"Time Out: {self.time_out_data}")
            # Save or process time_in and time_out data
            # For example:
            # self.save_to_database(self.time_in_data, self.time_out_data)
            self.time_in_data = None  # Reset time_in_data after processing
        else:
            messagebox.showwarning("Warning", "Please Time In first")

    def save_to_database(self, time_in, time_out):
        # Implement database save logic here
        pass

# Create the main window
root = Tk()
app = MyApp(root)
root.mainloop()
