from pathlib import Path

playback_url = "https://bbb.example.com/"

meeting_id = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-aaaaaaaaaaaaa"

data_dir = Path("./data")

fps = 5  # frames per second

pointer_size = 100

start = 10  # in seconds, set to None to start from the beginning
end = 100  # in seconds, set to None to convert until the end of the video

hide_pointer_if_offscreen = False

# set to "previous" or "next" for raw position data
# set to "linear" for linear interpolation
# set to "quadratic" for quadratic interpolation (needs hide_pointer_if_offscreen = False)
interpolation_method = "quadratic"
