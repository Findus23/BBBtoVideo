from pathlib import Path

import requests

from config import data_dir, meeting_id, playback_url


def fetch_file(path: str, show_progress=False) -> Path:
    local_file = data_dir / meeting_id / path
    if local_file.exists():
        return local_file
    else:
        print("downloading", path)
        data_url = f"{playback_url}presentation/{meeting_id}/{path}"
        local_file.parent.mkdir(parents=True, exist_ok=True)
        r = requests.get(data_url)
        r.raise_for_status()
        file_size = int(r.headers.get("content-length"))
        progress = 0
        with local_file.open("wb") as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
                progress += 128
                if show_progress:
                    print(f"Progress: {progress / file_size * 100:.2f}%", end="\r", flush=True)
        if show_progress:
            print()  # flush new line
        return local_file
