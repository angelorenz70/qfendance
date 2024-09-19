import face_recognition
import os
from concurrent.futures import ThreadPoolExecutor

# Function to process a single image
def process_image(image_path):
    try:
        # Load the image file
        decode_picture = face_recognition.load_image_file(image_path)
        
        # Find face locations
        face_locations = face_recognition.face_locations(decode_picture)
        
        if len(face_locations) > 0:
            # Encode the first face found
            face_encode = face_recognition.face_encodings(decode_picture, known_face_locations=face_locations)[0]
            getName = os.path.basename(image_path).split(',')[0]
            print(f'Face encoded for {getName}')
            return (getName, face_encode)
        else:
            print(f'No face found in {image_path}')
            return None
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def set_faces():
    # Path to the folder containing the images
    image_folder_path = "images/"

    # List to store encoded faces and their names
    faces = []

    # Get all image file paths
    image_paths = [os.path.join(image_folder_path, f) for f in os.listdir(image_folder_path)]

    # Process images in parallel
    with ThreadPoolExecutor() as executor:
        results = executor.map(process_image, image_paths)

    # Collect valid results
    faces = [res for res in results if res is not None]

    return faces

faces = set_faces()
