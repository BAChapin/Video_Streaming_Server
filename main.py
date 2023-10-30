# import io
# from flask import Flask, Response
# from picamera2 import Picamera2
# from picamera2.outputs import FileOutput
# from picamera2.encoders import JpegEncoder

# app = Flask(__name__)
# camera = None
# streaming = False
# connection_count = 0  # Counter to monitor active connections

# def generate_frames():
#     global camera, streaming

#     while streaming:
#         if camera is not None:
#             with io.BytesIO() as stream:
#                 output = FileOutput(stream)
#                 camera.start_recording(JpegEncoder(), output)

#                 # for _ in camera.capture_continuous(stream, format="jpeg", use_video_port=True):
#                 stream.seek(0)
#                 yield (b"--frame\r\n"
#                         b"Content-Type: image/jpeg\r\n\r\n" + stream.read() + b"\r\n")
#                 stream.seek(1)
#                 stream.truncate()

# @app.route('/video')
# def video():
#     global camera, streaming, connection_count

#     if not streaming:
#         camera = Picamera2()
#         camera.configure(camera.create_video_configuration(main={"size": (640, 480)}))
#         streaming = True

#     connection_count += 1
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/stop')
# def stop():
#     global camera, streaming, connection_count

#     if streaming:
#         if camera is not None:
#             camera.stop()
#             camera.stop_encoder()
#         streaming = False
#     connection_count = 0

#     return "Video stream stopped."

# @app.route('/connections')
# def get_connection_count():
#     return f"Active Connections: {connection_count}"

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', debug=True)

import cv2
import numpy
from flask import Flask, render_template, Response, stream_with_context, Request

video = cv2.VideoCapture(0)
app = Flask(__name__)

def video_stream():
    while(True):
        ret, frame = video.read()
        if not ret:
            break
        else:
            ret, buffer = cv2.imencode('.jpeg',frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/siteTest')

def siteTest():
    return render_template('siteTest.html')

@app.route('/video_feed')

def video_feed():
    return Response(video_stream(), mimetype= 'multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host ='0.0.0.0', port= '5000', debug=False)