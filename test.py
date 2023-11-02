from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder

picam2 = Picamera2()
video_config = picam2.video_configuration({"size": (1920, 1080)},
                                          raw={"size": (1640, 1232)},
                                          controls={"FrameDurationLimits": (33333, 33333)})
picam2.configure(video_config)
encoder = H264Encoder(40000000, False, 10)	# bitrate, repeat, iperiod
picam2.start_recording(encoder, 'test.h264')