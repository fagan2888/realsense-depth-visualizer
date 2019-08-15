import numpy as np
import pickle

from RealSenseCamera import RealSenseCamera

k = RealSenseCamera(serial_no='834412071881')
k.start()
frames = []

try:
    while True:
        image_dict = k.get_feed()[1]
        color_image = image_dict['color_image']
        depth_image = image_dict['depth_image']
        frames.append(image_dict)

except KeyboardInterrupt:
    frames = np.asarray(frames)
    # open a file, where you ant to store the data
    file = open('real_record.pkl', 'wb')

    # dump information to that file
    pickle.dump(frames, file)
