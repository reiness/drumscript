# src/separate_drums.py

import os
from pathlib import Path
from spleeter.separator import Separator
from src.utils.io_utils import download_youtube
import logging

logging.basicConfig(level=logging.INFO)

def isolate_drums(input_path: str, output_dir: str) -> str:
    local = download_youtube(input_path) if input_path.startswith('http') else input_path

    # ← use 4-stem model to get drums.wav
    sep = Separator('spleeter:4stems')
    sep.separate_to_file(local, output_dir)

    stem_dir = Path(output_dir) / Path(local).stem
    drum_path = stem_dir / 'drums.wav'
    if not drum_path.exists():
        logging.error(f"❌ drums.wav not created at {drum_path}")
    else:
        logging.info(f"✅ drums.wav created at {drum_path}")
    return str(drum_path)
