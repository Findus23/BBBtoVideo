# BBBtoVideo

> Download BigBlueButton recordings and convert them to videos

## Dependencies (Debian packages):
- python3
- requests (`python3-requests`) for downloading files
- OpenCV (`python3-opencv`) for creating a video from still images
- numpy (`python3-numpy`) for drawing the cursor
- syipy (`python3-scipy`) for interpolating the position of the cursor
- ffmpeg (`ffmpeg`) for merging audio and video

## How to use

If your BBB recording URL looks like this 

```text
https://bbb.example/playback/presentation/2.0/playback.html?meetingId=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-aaaaaaaaaaaaa
```

then copy the `config.sample.py` to `config.py` and set the variables like this:

```python
playback_url = "https://bbb.example/"

meeting_id = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-aaaaaaaaaaaaa"
```

and run the `main.py`.
It should download all required files into a `data/` directory and create a `without_audio.mp4` that is just the slides and cursor and a `output.mp4` that also contains the audio.

## Limitations
- no screen-sharing support
- no webcam support
- no support for zooming into pages
