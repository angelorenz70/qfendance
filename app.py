from flask import Flask, Response, render_template, jsonify, flash, send_from_directory
from face_detection import FaceDetection
from qrcode_scanner import decoder
import cv2
from datetime import datetime
from app_dbconnection import DbConnection

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# Initialize the camera
camera = cv2.VideoCapture(0)  # 0 for the default camera
camera_mode = "check_in"
flash_message_triggered = False  # Flag for alert
qr_data = None



def generate_frames():
    global flash_message_triggered, qr_data
    face_detection = FaceDetection()
    db = DbConnection()

    while True:
        success, frame = camera.read()  # Read a frame from the camera
        

        if not success:
            break

        frame = cv2.flip(frame, 1)
        # Define square parameters (top-left corner and side length)
        x, y = 100, 100  # Coordinates of the top-left corner
        side_length = 200  # Length of each side of the square

        # Draw a red square (BGR color format: blue, green, red)
        color = (0, 0, 255)  # Red color in BGR
        thickness = 2  # Line thickness (negative thickness means filled)
        cv2.rectangle(frame, (x, y), (x + side_length, y + side_length), color, thickness)

        # Detect face in the frame
        face_detected = face_detection.detect(frame)

        if face_detected:
            frame, barcode_data = decoder(frame)
            data = str(barcode_data)
            if len(data) > 0:
                time = datetime.now().time()
                created_at = datetime.now()
                ready_data = [camera_mode, data, time, created_at] #camera mode for time_mode, qr_data for id_number data, date, created_at
                db.insert(ready_data, frame)
                qr_data = data
                flash_message_triggered = True  # Set the flag for flash message
                cv2.putText(frame, f"{qr_data} -> Face Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                # print(camera_mode)
            else:
                flash_message_triggered = False
                cv2.putText(frame, "No QR code -> Face Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                # print(camera_mode)
        else:
            cv2.putText(frame, "No Face Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            # print(camera_mode)
            flash_message_triggered = False

        # Encode the frame in JPEG format
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()  # Convert to bytes

        # Yield the frame for streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/flash_message', methods=['GET'])
def flash_message():
    global flash_message_triggered  # Make sure to access the global flag
    global qr_data

  

    if flash_message_triggered:
        # flash("Face and QR Code detected!")
        flash_message_triggered = False  # Reset the flag after processing
        return jsonify({"status": "Success", 'date': f'{datetime.now().date()}', 'time': f'{datetime.now().strftime("%H:%M:%S")}', 'time_mode': f'{camera_mode}', 'qrcode_data' : f'{qr_data}'}), 200
    else:
        return jsonify({"status": "Failed"}), 200
    


@app.route('/video_feed')
def video_feed():
    # Return the response as a multipart stream
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    db = DbConnection()
    entries = db.fetch_latest_entries(limit=5)  # Fetch the latest 5 entrie
    return render_template('index.html',  entries=entries)

@app.route('/set_mode/<mode>')
def set_mode(mode):
    global camera_mode
    camera_mode = mode  # Update the global camera mode
    print(str(camera_mode).replace("_", " "))
    return jsonify({"current_mode": str(camera_mode).replace("_", " ")})

@app.route('/app_attendance_pictures/<path:filename>')
def serve_image(filename):
    return send_from_directory('app_attendance_pictures', filename)

@app.route('/update_table')
def update_table():
    db = DbConnection()
    entries = db.fetch_latest_entries(limit=5)
    return render_template('time_tracking.html', entries=entries)

if __name__ == '__main__':
    db = DbConnection()
    app.run(host='0.0.0.0', port=5000)
