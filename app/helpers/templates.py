"""
Imports
"""
from moviepy.editor import ColorClip
import math
import numpy as np

from helpers import constants


"""
Constants
"""
ABSOLUTE_FILEPATH = constants.absolute_filepath()


"""
create blank white videos to be used as templates
"""
def generate_templates(start_time, end_time,
                       increment,
                       height, width=1080):

    height = height
    width = width
    video_fps = 30
    colour = (255, 255, 255)
    dest = f"{ABSOLUTE_FILEPATH}resources/videos/templates/{height}x{width}/"

    # Get numpy array of all video lengths
    video_durations = np.arange(start_time, end_time, increment)

    # Create all videos
    for dur in video_durations:
        dur = round_down_duration(dur)
        ColorClip((width, height), duration=dur, color=colour).write_videofile(
            dest + str(dur) + ".mp4", fps=video_fps, logger=None)


"""
Rounds down
# 0.1 to 4.9, rounds down 0.1
# 5.0 to 9.8, rounds down 0.2
# 10.0 to 29.75, rounds down 0.25
# 30.0 to 59.5, rounds down 0.5
# TODO: 60 to 180, round down 1.0
"""
def round_down_duration(num):
    if num >= 0.1 and num <= 5.0:
        num = math.floor(num / 0.1) * 0.1
        return float("{:.1f}".format(num))

    elif num >= 5.2 and num <= 10.0:
        num = math.floor(num / 0.2) * 0.2
        return float("{:.1f}".format(num))

    elif num >= 10.25 and num <= 30.0:
        num = math.floor(num / 0.25) * 0.25
        return float("{:.2f}".format(num))

    elif num >= 30.5 and num <= 60.0:  # excludes 60.0
        num = math.floor(num / 0.5) * 0.5
        return float("{:.2f}".format(num))

    else:
        print("video too long")


"""
Generate all blank videos
"""
def generate_all_templates():
    generate_templates(0.1, 5.0, 0.1, 1920)
    generate_templates(5.0, 10.0, 0.2, 1920)
    generate_templates(10.0, 30.0, 0.25, 1920)
    generate_templates(30.0, 60.0, 0.5, 1920)


"""
Generate blank video of specific length
"""
def generate_one_template(start_time, end_time, increment, height):
    generate_templates(start_time, end_time, increment, height)
