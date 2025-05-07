# src/utils/io_utils.py

import os
from pytube import YouTube  # or youtube_dl, whichever you prefer

def download_youtube(url: str, output_dir: str = '.') -> str:
    """
    Download a YouTube video’s audio as an MP3 (or WAV) and return the filepath.
    """
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    out_path = stream.download(output_dir)
    # If it’s mp4, rename to .mp3 or .wav here if you like
    base, ext = os.path.splitext(out_path)
    target = base + '.mp3'
    os.rename(out_path, target)
    return target
