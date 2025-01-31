from moviepy import *
from datetime import timedelta

video = VideoFileClip("filme.mp4")

start_time = timedelta(minutes=20).total_seconds()
end_time = timedelta(minutes=21).total_seconds()

cut_video = video.subclipped(start_time, end_time)

cut_video.write_videofile("corte_movie.mp4", codec="libx264")