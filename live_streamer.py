import time
from flask import Flask, Response
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

app = Flask(__name__)

picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"size": (640, 480)})
picam2.configure(video_config)

encoder = H264Encoder(bitrate=16000, qp=30)

output = FfmpegOutput("-f hls -hls_time 5 -hls_list_size 2 -hls_flags delete_segments -hls_allow_cache 5 stream.m3u8")

@app.route('/video')
def video():
    m3u8 = f'#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-TARGETDURATION:5\n#EXT-X-MEDIA-SEQUENCE:0\n#EXTINF:5,\n/video/0\n'
    return Response(m3u8, content_type='Application/vnd.apple.mpegurl')

@app.route('/video/<segment>')
def video_segment(segment):
    segment_number = int(segment)
    with open(f'stream{segment_number}.ts', 'rb') as segment_file:
        data = segment_file.read()
    yield data

if __name__ == '__main__':
    picam2.start_recording(encoder, output)
    # time.sleep(30)
    # picam2.stop_recording()
    app.run(host='0.0.0.0', port=5000, debug=True)