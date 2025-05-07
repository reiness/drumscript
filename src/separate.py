import os
import subprocess
from pathlib import Path
from src.utils.io_utils import download_youtube
import logging

logging.basicConfig(level=logging.INFO)

def isolate_drums(input_path: str, output_dir: str) -> str:
    """
    Download (if YouTube URL) and separate with Demucs 6-source model.
    Returns path to drums.wav.
    """
    # 1) fetch local file
    local = download_youtube(input_path) if input_path.startswith('http') else input_path
    stem_name = Path(local).stem

    # 2) ensure output dir exists
    outdir = Path(output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    # 3) run demucs CLI with 6-source model
    temp_outdir = outdir / "htdemucs_6s"
    cmd = [
        "demucs",
        "--name", "htdemucs_6s",
        "--out", str(outdir),
        str(local)
    ]
    logging.info(f"🛠 Running Demucs 6-stems: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        logging.error("❌ demucs not found on PATH. Install with `pip install demucs`.")
        raise
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Demucs failed: {e}")
        raise

    # 4) move htdemucs_6s/<track>/ → output_dir/<track>/
    src_stem_dir = temp_outdir / stem_name
    dst_stem_dir = outdir / stem_name
    if dst_stem_dir.exists():
        logging.warning(f"⚠️ Overwriting existing output folder: {dst_stem_dir}")
    src_stem_dir.rename(dst_stem_dir)

    # 5) locate drums stem
    drums_path = dst_stem_dir / "drums.wav"
    if not drums_path.exists():
        logging.error(f"❌ drums.wav not created at {drums_path}")
        raise FileNotFoundError(f"Expected drums stem at {drums_path}")
    logging.info(f"✅ drums.wav created at {drums_path}")

    return str(drums_path)



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Download (or load) a track and separate its drums using Demucs 6-source."
    )
    parser.add_argument("input", help="YouTube URL or local audio file")
    parser.add_argument(
        "--out", "-o", default="separated",
        help="Directory to write stems into"
    )
    args = parser.parse_args()
    isolate_drums(args.input, args.out)
