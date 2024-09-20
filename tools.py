import tkinter as tk
import cv2
import numpy as np
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
from datetime import datetime

class Button:
    def __init__(self, frame, text, command) -> None:
        self.button = tk.Button(
            frame,
            text=text,
            command=command,
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

class AddText:
    def __init__(self) -> None:
        pass

    def add_text_to_image(self, frame, name, id, datetime, camera_mode):
        # Convert OpenCV image (BGR) to PIL image (RGB)
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_image)

        # Create a drawing context
        draw = ImageDraw.Draw(pil_image)

        # Define font and size (you can adjust the path and size as needed)
        font = ImageFont.load_default()
        
        if camera_mode == 'time_in':    
            text = f"Name: {name}\nID: {id}\nTime In: {datetime.now()}"
        elif camera_mode == 'break_out':
            text = f"Name: {name}\nID: {id}\nBreak Out: {datetime.now()}"
        elif camera_mode == 'break_in':
            text = f"Name: {name}\nID: {id}\nBreak In: {datetime.now()}"
        elif camera_mode == 'time_out':
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
    
class SaveImage:
    def __init__(self) -> None:
        pass

    # Function to save the current frame
    def save(self, current_frame, current_name, global_id, global_name, camera_mode):
        if current_frame is not None:

            # Ensure the 'pictures' directory exists
            folder_path = f'pictures/{datetime.now().date()}/{camera_mode}'
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            
            #Create a unique file name with a timestamp
            file_name = f'{folder_path}/{current_name},{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            #add text to a frame
            addtext = AddText()
            frame = addtext.add_text_to_image(current_frame,global_name, global_id, datetime.now(), camera_mode)

            # Save the current frame as a PNG file
            cv2.imwrite(file_name, frame)
            print(f'Frame saved as {file_name}')
        else:
            print('No frame available to save')

