import subprocess
from pathlib import Path
from typing import Optional

import cv2
import numpy as np

from config import fps, pointer_size, start, end
from cursor import Cursor
from download import fetch_file
from metadata import Metadata
from shapes import Shapes

metadata = Metadata(fetch_file("metadata.xml"))

print(f'found "{metadata.meetingName}"')
print(f"starting on {metadata.starttime}")

cursor = Cursor(fetch_file("cursor.xml"))

shapes = Shapes(fetch_file("shapes.svg"))
for slide in shapes.slides:
    a = slide.file  # pre-download slide images

audio = fetch_file("video/webcams.webm", show_progress=True)

print("start generating video")
if start is None:
    time = 0
else:
    time = start
if end is None:
    end = metadata.duration
    print(end)
frame_len = 1 / fps
slide_id = -1
video_file = Path("without_audio.mp4")
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
print(shapes.maxwidth, shapes.maxheight)
out = cv2.VideoWriter(str(video_file), fourcc, fps, (shapes.maxwidth, shapes.maxheight))
slide = shapes.slides[0]
image: Optional[np.ndarray] = None
print()

while time <= end:
    frame = np.zeros((shapes.maxheight, shapes.maxwidth, 3))

    while time > slide.end or image is None:
        slide_id += 1
        slide = shapes.slides[slide_id]
        image: np.ndarray = cv2.imread(str(slide.file))
    frame[0:slide.height, 0:slide.width] = image
    x_frac = cursor.xspline(time)
    y_frac = cursor.yspline(time)
    if not (np.isnan(x_frac) or np.isnan(y_frac)):
        cursor_x = int(round(x_frac * slide.width))
        cursor_y = int(round(y_frac * slide.height))
        if -pointer_size <= cursor_x <= slide.width + pointer_size and -pointer_size <= cursor_y <= slide.height + pointer_size:
            frame[cursor_y - pointer_size:cursor_y + pointer_size,
            cursor_x - pointer_size:cursor_x + pointer_size] = np.array([0, 0, 255], dtype=np.uint8)
    else:
        cursor_x = None
        cursor_y = None
    print(f"{time:.2f}/{end:.2f} {slide_id} {cursor_x} {cursor_y}                 ", end="\r", flush=True)

    out.write(frame.astype(np.uint8))

    time += frame_len

out.release()
print()

command = [
    "ffmpeg", "-i", str(video_file), "-ss", str(start), "-to", str(end), "-i", str(audio), "-ss", str(0), "-c",
    "copy",
    "output.mp4",
    "-y"
]
print("merge video with audio")
print(" ".join(command))
subprocess.run(command)
