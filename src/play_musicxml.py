import time
import argparse
from pathlib import Path
from music21 import converter, chord
import simpleaudio as sa

# Map your MusicXML part-names to WAV filenames (in your samples dir)
PART_SAMPLES = {
    'KICK':  'kick.wav',        # part-name “KICK”
    'SNARE': 'snare.wav',       # part-name “SNARE”
    'HIHAT': 'hihat.wav',       # part-name “HIHAT”
    # 'OPEN_HIHAT': 'hihat_open.wav',  # e.g. if you have a part named “OPEN_HIHAT”
    # 'CRASH': 'crash.wav',
}


def load_samples(sample_dir: Path, part_map: dict) -> dict:
    """
    Load WAVs, returning part-name -> WaveObject.
    """
    waves = {}
    for part_name, fname in part_map.items():
        path = sample_dir / fname
        if not path.exists():
            print(f"⚠️ Missing sample for part {part_name}: {path}")
            continue
        waves[part_name] = sa.WaveObject.from_wave_file(str(path))
    return waves


def get_tempo_and_qsec(score) -> tuple:
    """
    Extract tempo (BPM) or default to 120, then seconds per quarter-note.
    """
    marks = score.metronomeMarkBoundaries()
    bpm = marks[0][2].number if marks else 120
    return bpm, 60.0 / bpm


def schedule_events(score, waves: dict, qsec: float) -> list:
    """
    For each part whose name matches a sample, schedule every Note/Chord.
    Returns a sorted list of (time, WaveObject).
    """
    events = []
    for part in score.parts:
        name = (part.partName or "").strip().upper()
        if name not in waves:
            continue

        wave = waves[name]
        # schedule all single notes
        for n in part.flat.getElementsByClass('Note'):
            start = float(n.offset) * qsec
            events.append((start, wave))

        # schedule one hit per chord
        for c in part.flat.getElementsByClass('Chord'):
            start = float(c.offset) * qsec
            events.append((start, wave))

    events.sort(key=lambda x: x[0])
    return events


def play_events(events: list):
    """
    Play scheduled events in real time.
    """
    if not events:
        print("⚠️ No drum events to play.")
        return

    print(f"▶️ Playing {len(events)} hits...")
    t0 = time.time()
    idx = 0
    while idx < len(events):
        now = time.time() - t0
        event_time, wave = events[idx]
        if now >= event_time:
            wave.play()
            idx += 1
        else:
            # sleep up to next event (or 5ms)
            time.sleep(min(0.005, event_time - now))


def main(xml_path: str, samples_dir: str):
    xml_file = Path(xml_path)
    sample_dir = Path(samples_dir)

    if not xml_file.exists():
        raise FileNotFoundError(f"MusicXML not found: {xml_file}")
    if not sample_dir.exists():
        raise FileNotFoundError(f"Samples dir not found: {sample_dir}")

    print(f"📖 Loading MusicXML: {xml_file}")
    score = converter.parse(str(xml_file))

    print(f"🔊 Loading samples from: {sample_dir}")
    waves = load_samples(sample_dir, PART_SAMPLES)

    bpm, qsec = get_tempo_and_qsec(score)
    print(f"⏱ Tempo: {bpm} BPM, quarter-note = {qsec:.3f}s")

    events = schedule_events(score, waves, qsec)
    play_events(events)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Play percussion-only MusicXML by mapping parts to samples.'
    )
    parser.add_argument('xml', help='Path to MusicXML file')
    parser.add_argument(
        '--samples', default='samples',
        help='Directory containing WAV samples'
    )
    args = parser.parse_args()
    main(args.xml, args.samples)
