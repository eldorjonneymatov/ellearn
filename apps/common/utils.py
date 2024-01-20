import re
from moviepy.editor import VideoFileClip

def calculate_reading_time(content, words_per_minute=200):
    words = re.findall(r'\b\w+\b', content)
    word_count = len(words)

    minutes = word_count / words_per_minute

    return round(minutes) if round(minutes) > 0 else 1

def get_video_length(path):
    try:
        clip = VideoFileClip(path)
        duration_in_seconds = clip.duration
        clip.close()
        return duration_in_seconds
    except:
        return None