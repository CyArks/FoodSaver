# app.py
from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def generate_frames():
    # Open a video capture stream, you can use a webcam or IP camera URL here
    cap = cv2.VideoCapture(0)

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            if ret:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def writeProductInformationToDB():
    ProductName = None
    Type = None
    Weight = None
    ExpirationDate = None
    Category = None
    MeasurementUnit = None


if __name__ == '__main__':
    app.run(debug=True)
