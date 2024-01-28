import math
import re

import html2text
from moviepy.editor import VideoFileClip


def calculate_reading_time(content, words_per_minute=200):
    text = html2text.html2text(content)
    text = re.sub(r"\s+", " ", text)
    words = text.split(" ")
    return math.ceil(len(words) / words_per_minute)


def get_video_length(path):
    try:
        clip = VideoFileClip(path)
        duration_in_seconds = clip.duration
        clip.close()
        return math.ceil(duration_in_seconds / 60)
    except Exception as e:
        print(e)
        return None
