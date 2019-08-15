import numpy as np

from colour import Color

VIZ_COLORS_BPBGYORW = []
VIZ_COLORS_BPBGYORW.extend(list(Color("black").range_to(Color("purple"), 15)))
VIZ_COLORS_BPBGYORW.extend(list(Color("purple").range_to(Color("blue"), 15)))
VIZ_COLORS_BPBGYORW.extend(list(Color("blue").range_to(Color("green"), 15)))
VIZ_COLORS_BPBGYORW.extend(list(Color("green").range_to(Color("yellow"), 15)))
VIZ_COLORS_BPBGYORW.extend(list(Color("yellow").range_to(Color("orange"), 15)))
VIZ_COLORS_BPBGYORW.extend(list(Color("orange").range_to(Color("red"), 15)))
VIZ_COLORS_BPBGYORW.extend(list(Color("red").range_to(Color("white"), 15)))


class HeatMapVisualizer():


    def __init__(self, upper_cutoff=65535, lower_cutoff=0, colors=VIZ_COLORS_BPBGYORW):
        self.__upper_cutoff = upper_cutoff
        self.__lower_cutoff = lower_cutoff
        self.__colors = colors

        self.__num_segments = len(colors)
        self.__segment_range = (upper_cutoff - lower_cutoff) / self.__num_segments

    def get_image_map(self, depth_image):
        heat_map = np.zeros((depth_image.shape[0],depth_image.shape[1],3))
        cutoff_high = self.__upper_cutoff

        for i in range(self.__num_segments):
            cutoff_low = cutoff_high - self.__segment_range
            mask = (depth_image < cutoff_high) & (depth_image > cutoff_low)
            heat_map[mask] = (self.__colors[i].get_blue() * 255, self.__colors[i].get_green() * 255, self.__colors[i].get_red() * 255)
            cutoff_high = cutoff_low

        mask = (depth_image < cutoff_high) & (depth_image > 0)
        heat_map[mask] = (self.__colors[self.__num_segments - 1].get_blue() * 255, self.__colors[self.__num_segments - 1].get_green() * 255,
                           self.__colors[self.__num_segments - 1].get_red() * 255)

        mask = depth_image <= 0
        heat_map[mask] = (self.__colors[0].get_blue() * 255, self.__colors[0].get_green() * 255, self.__colors[0].get_red() * 255)

        return heat_map


