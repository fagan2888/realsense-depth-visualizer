from threading import Thread

import cv2
from py_pipe.pipe import Pipe
import pyrealsense2 as rs
import numpy as np


class RealSenseCamera(object):

    def __init__(self, serial_no, fps=30, hxw=(640, 480)):
        self.pipe = Pipe(limit=1)
        self.serial_no = serial_no
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.fps = fps
        self.hxw = hxw
        self.obj = None

    def __start(self):
        # initialise camera
        print('ser = ', self.serial_no)
        self.config.enable_device(self.serial_no)
        self.config.enable_stream(rs.stream.depth, self.hxw[0], self.hxw[1], rs.format.z16, self.fps)
        self.config.enable_stream(rs.stream.color, self.hxw[0], self.hxw[1], rs.format.bgr8, self.fps)


        self.pipeline.start(self.config)

        align_to = rs.stream.color
        align = rs.align(align_to)

        try:
            while True:
                # Wait for a coherent pair of frames: depth and color
                frames = self.pipeline.wait_for_frames()
                aligned_frames = align.process(frames)

                depth_frame = aligned_frames.get_depth_frame().as_depth_frame()
                color_frame = frames.get_color_frame()

                # Validate that both frames are valid
                if not depth_frame or not color_frame:
                    continue

                # Convert images to numpy arrays
                depth_image = np.asanyarray(depth_frame.get_data())
                color_image = np.asanyarray(color_frame.get_data())

                self.pipe.push_wait()
                self.pipe.push({"color_image": color_image, "depth_image": depth_image})

        finally:
            # Stop streaming
            self.pipeline.stop()

    def start(self):
        Thread(target=self.__start).start()

    def get_feed(self):
        self.pipe.pull_wait()
        feed = self.pipe.pull()
        return feed

    def stop_feed(self):
        self.pipeline.stop()

    def skip_Nframes(self, count):
        counter = 0
        while counter < count:
            feed = self.get_feed()
            counter += 1

# k = RealSenseCamera(serial_no='834412071881')
# k.start()
#
# # REAL_SENSE_CAMERAS = {'836313022053' : '834412071229', '836313021550' : '834412071881' }
#
# while True:
#     dict = k.get_feed()[1]
#     color_image = dict['color_image']
#     depth_image = dict['depth_image']
#     cv2.imshow('color', color_image)
#     print(' depth at pixel (250,375) : ',depth_image[250][375]/1000)
#     cv2.waitKey(1)
