# from flask import Flask, Response
# import subprocess

# app = Flask(__name__)

# @app.route('/video.m3u8')
# def video():
#     return Response(generate_m3u8(), content_type='application/vnd.apple.mpegurl')

# @app.route('/video/<segment>')
# def video_segment(segment):
#     return Response(generate_video_segment(segment), content_type='video/mp2t')

# def generate_m3u8():
#     m3u8 = f'#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-TARGETDURATION:10\n#EXT-X-MEDIA-SEQUENCE:0\n#EXTINF:10.0,\n/video/0.ts\n'
#     return m3u8

# def generate_video_segment(segment):
#     segment_number = int(segment.split('.')[0])
#     while True:
#         command = [
#             'ffmpeg',
#             '-s', '640x580',  # Set the video resolution
#             '-i', '/dev/video0',  # Input source (Raspberry Pi camera module)
#             '-f', 'mpegts',
#             '-c:v', 'h264_omx',
#             '-b:v', '1M',  # Video bitrate (adjust as needed)
#             '-tune', 'zerolatency',
#             '-r', '30',  # Frames per second (adjust as needed)
#             '-g', '60',
#             '-y',
#             '-segment_list', 'playlist.m3u8',
#             '-segment_list_flags', '+live',
#             '-segment_time', '10',  # Segment duration in seconds
#             f'segment{segment_number}.ts',
#         ]

#         subprocess.run(command)
#         with open(f'segment{segment_number}.ts', 'rb') as segment_file:
#             data = segment_file.read()
#         yield data

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)

from flask import Flask, Response
import subprocess

app = Flask(__name__)

@app.route('/stream.m3u8')
def stream():
    return Response(generate_m3u8(), content_type='application/vnd.apple.mpegurl')

@app.route('/stream/<segment>')
def video_segment(segment):
    return Response(generate_video_segment(segment), content_type='video/mp2t')

def generate_m3u8():
    m3u8 = f'#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-TARGETDURATION:10\n#EXT-X-MEDIA-SEQUENCE:0\n#EXTINF:10.0,\n/stream/0.ts\n'
    return m3u8

def generate_video_segment(segment):
    segment_number = int(segment.split('.')[0])
    while True:
        command = [
            'ffmpeg',
            '-i', 'your_input_video.mp4',  # Specify your input video file
            '-map', '0',
            '-f', 'segment',
            '-segment_time', '10',  # Segment duration in seconds
            '-segment_format', 'mpegts',
            f'stream/{segment_number}.ts',
        ]

        subprocess.run(command)
        with open(f'stream/{segment_number}.ts', 'rb') as segment_file:
            data = segment_file.read()
        yield data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
