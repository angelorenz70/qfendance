import cv2
import face_recognition
import os
import numpy as np
from pyzbar.pyzbar import decode

def decoder(image):
    gray_img = cv2.cvtColor(image,0)
    barcode = decode(gray_img)

    for obj in barcode:
        points = obj.polygon
        (x,y,w,h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)

        barcodeData = obj.data.decode("utf-8")
        barcodeType = obj.type
        string = "Data: " + str(barcodeData) + " | Type: " + str(barcodeType)
        
        cv2.putText(frame, string, (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255), 2)
        print("Barcode: "+barcodeData +" | Type: "+barcodeType)

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    decoder(frame)
    cv2.imshow('Image', frame)
    code = cv2.waitKey(10)
    if code == ord('q'):
        break


# # Path to the folder containing the images
# image_folder_path = "images/"

# # List to store encoded faces and their names
# faces = []

# # Encode and decode all faces
# for filename in os.listdir(image_folder_path):
#     image_path = os.path.join(image_folder_path, filename)
    
#     # Load the image file
#     decode_picture = face_recognition.load_image_file(image_path)
    
#     # Find face locations
#     face_locations = face_recognition.face_locations(decode_picture)
    
#     if len(face_locations) > 0:
#         # Encode the first face found
#         face_encode = face_recognition.face_encodings(decode_picture, known_face_locations=face_locations)[0]
#         getName = filename.split(',')
#         faces.append([getName[0], face_encode])  # [0][0] - name, [0][1] - frame
#         print(f'Face encoded for {filename}')
#     else:
#         print(f'No face found in {filename}')

# # Define a video capture object
# vid = cv2.VideoCapture(0)

# # Declare the width and height in variables
# width, height = 1000, 500

# # Set the width and height
# vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
# vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# # Check if the camera opened successfully
# if not vid.isOpened():
#     print("Error: Could not open camera.")
#     exit()

# # Loop to continuously capture frames from the camera
# while True:
#     # Capture each frame
#     ret, frame = vid.read()
    
#     if ret:
#         # Try to find face encodings in the current frame
#         face_encodings = face_recognition.face_encodings(frame)
        
#         # Check if at least one face encoding was found
#         if len(face_encodings) > 0:
#             unknown_face_encoding = face_encodings[0]  # Take the first detected face encoding

#             # Compare detected face with known faces
#             for face in faces:
#                 results = face_recognition.compare_faces([face[1]], unknown_face_encoding)
#                 if results[0]:
#                     print(f'I am {face[0]}')
#                     cv2.putText(frame, f'name: {face[0]}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
#                     break
#             else:
#                 # If no matches are found
#                 print("It's not a picture of me!")
#                 cv2.putText(frame, "Unknown", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
#         else:
#             # No faces detected
#             print("No face detected.") 
#             cv2.putText(frame, "No face detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

#         # Display the frame with text
#         cv2.imshow('Camera Live Feed', frame)
#     else:
#         print("Error: Failed to capture frame.")
#         break

#     # Wait for 1ms and check if 'q' is pressed to exit
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the camera and close all OpenCV windows
# vid.release()
# cv2.destroyAllWindows()


