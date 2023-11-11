import time
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"size": (640, 480)})
picam2.configure(video_config)

encoder = H264Encoder(bitrate=16000, qp=30)

output = FfmpegOutput("-f hls -hls_time 5 -hls_list_size 10 -hls_flags delete_segments -hls_allow_cache 5 stream.m3u8")

picam2.start_recording(encoder, output)
time.sleep(30)
picam2.stop_recording()