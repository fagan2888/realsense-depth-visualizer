import numpy as np

import cv2
from flask import Flask, render_template, request
from flask_cors import CORS
from py_flask_movie.flask_movie import FlaskMovie
from py_pipe.pipe import Pipe

from RealSenseCamera import RealSenseCamera
from heatmap_visualization import HeatMapVisualizer

app = Flask(__name__)
CORS(app)

fmovie = FlaskMovie(app)

color_pipe = Pipe(limit=1)
depth_pipe = Pipe(limit=1)

fmovie.create('color_feed', color_pipe)
fmovie.create('depth_feed', depth_pipe)


@app.route('/')
def index_html():
    return render_template('index.html')


upper_cutoff = 2000
lower_cutoff = 1000


@app.route('/update', methods=['POST', 'GET'])
def controls():
    global upper_cutoff, lower_cutoff
    uc = request.args.get('upper_cutoff')
    if uc:
        upper_cutoff = int(uc)
    lc = request.args.get('lower_cutoff')
    if lc:
        lower_cutoff = int(lc)
    return request.query_string


fmovie.start(bind_ip='0.0.0.0', bind_port=5000)

k = RealSenseCamera(serial_no='834412071881')
k.start()

while True:
    image_dict = k.get_feed()[1]
    color_image = image_dict['color_image']
    depth_image = image_dict['depth_image']

    HMV = HeatMapVisualizer(upper_cutoff=upper_cutoff, lower_cutoff=lower_cutoff)
    depth_map = HMV.get_image_map(depth_image)

    depth_pipe.push(depth_map)
    color_pipe.push(color_image)

    # cv2.imwrite('images/depth_image'+str(img_number).zfill(5)+'.png', depth_map)
    # cv2.imwrite('images/color_image'+str(img_number).zfill(5)+'.png', color_image)
    # img_number += 1
