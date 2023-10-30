import io
import picamera
from flask import Flask, Response

app = Flask(__name__)
camera = None
streaming = False
connection_count = 0  # Counter to monitor active connections

def generate_frames():
    global camera, streaming
    while streaming:
        if camera is not None:
            with io.BytesIO() as stream:
                for _ in camera.capture_continuous(stream, format="jpeg", use_video_port=True):
                    stream.seek(0)
                    yield (b"--frame\r\n"
                           b"Content-Type: image/jpeg\r\n\r\n" + stream.read() + b"\r\n")
                    stream.seek(0)
                    stream.truncate()

@app.route('/video')
def video():
    global camera, streaming, connection_count

    if not streaming:
        camera = picamera.PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 30
        streaming = True

    connection_count += 1
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop')
def stop():
    global camera, streaming, connection_count

    if streaming:
        if camera is not None:
            camera.close()
        streaming = False
    connection_count = 0

    return "Video stream stopped."

@app.route('/connections')
def get_connection_count():
    return f"Active Connections: {connection_count}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
