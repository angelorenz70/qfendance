import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import mediapipe as mp

class FaceDetection:
    def __init__(self) -> None:
        self.base_options = python.BaseOptions(model_asset_path='face_landmarker.task')
        self.options = vision.FaceLandmarkerOptions(base_options=self.base_options,
                                            output_face_blendshapes=True,
                                            output_facial_transformation_matrixes=True,
                                            num_faces=1)
        self.detector = vision.FaceLandmarker.create_from_options(self.options)

    def detect(self, frame):
        frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        detection_result = self.detector.detect(frame)

        return detection_result.face_landmarks != []
    


# cap = cv2.VideoCapture(0)

# face_detection = FaceDetection()

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         print("Error: Failed to capture frame.")
#         break
    
#     detected, detection_result, frame = face_detection.detect(frame)

#     if detected:
#         print('FACE DETECTED')
#     else:
#         print('NO FACE DETECTED')


#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()