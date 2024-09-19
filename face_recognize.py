import face_recognition
import cv2
import os


def recognize_face(frame, faces):
    # Try to find face encodings in the current frame
    face_encodings = face_recognition.face_encodings(frame)
    person_name = '-'
    # Check if at least one face encoding was found
    if len(face_encodings) > 0:
        unknown_face_encoding = face_encodings[0]  # Take the first detected face encoding

        # Compare detected face with known faces
        for face in faces:
            results = face_recognition.compare_faces([face[1]], unknown_face_encoding)
            if results[0]:
                print(f'I am {face[0]}')
                cv2.putText(frame, f'name: {face[0]}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                person_name = face[0]
                break
        else:
            # If no matches are found
            print("It's not a picture of me!")
            cv2.putText(frame, "Unknown", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    else:
        # No faces detected
        print("No face detected.") 
        cv2.putText(frame, "No face detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    return frame, person_name