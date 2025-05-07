import os
from pathlib import Path
from music21 import converter, tempo, meter, stream

def midi_to_musicxml(midi_path: str, out_dir: str, input_name: str, bpm: float = None, ts: str = '4/4') -> str:
    """
    Convert a multi-instrument MIDI file to MusicXML with optional tempo and time signature.
    Returns the path to the generated .musicxml file.
    """
    # 1. Parse the MIDI file
    score = converter.parse(midi_path)

    # 2. Insert global tempo and time signature at the top of the score
    if bpm:
        mm = tempo.MetronomeMark(number=bpm)
        score.insert(0, mm)

    if ts:
        ts_obj = meter.TimeSignature(ts)
        score.insert(0, ts_obj)

    # 3. Quantize notes in all parts to nearest 1/16 for cleaner notation
    for part in score.parts:
        for n in part.recurse().notes:
            dur = n.duration
            dur.quarterLength = round(dur.quarterLength * 16) / 16
            n.duration = dur

    # 4. Ensure the output directory structure exists
    result_dir = os.path.join(out_dir, input_name)
    os.makedirs(result_dir, exist_ok=True)

    # 5. Write out MusicXML
    xml_path = os.path.join(result_dir, Path(midi_path).stem + '.musicxml')
    score.write('musicxml', fp=xml_path)

    return xml_path
