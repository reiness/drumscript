import os
from pathlib import Path
from music21 import converter, tempo, meter, note, stream

def midi_to_musicxml(midi_path: str, out_dir: str, input_name: str, bpm: float = None, ts: str = '4/4') -> str:
    """
    Convert a MIDI file to MusicXML with optional tempo and time signature.
    Returns the path to the generated .xml file.
    """
    # 1. Parse MIDI
    score = converter.parse(midi_path)

    # 2. Insert tempo mark if provided
    if bpm:
        mm = tempo.MetronomeMark(number=bpm)
        score.insert(0, mm)

    # 3. Insert time signature
    ts_obj = meter.TimeSignature(ts)
    score.insert(0, ts_obj)

    # 4. Quantize percussion part to nearest 16th note for clean notation
    #    (optional step—music21 does its own quantization, but this tightens it)
    part = score.parts[0]
    for n in part.recurse().notes:
        # snap offset to nearest 1/16
        dur = n.duration
        dur.quarterLength = round(dur.quarterLength * 16) / 16
        n.duration = dur

    # 5. Ensure the output directory structure exists
    result_dir = os.path.join(out_dir, input_name)  # Create a subfolder with input_name
    os.makedirs(result_dir, exist_ok=True)

    # 6. Write out MusicXML
    xml_path = os.path.join(result_dir, Path(midi_path).stem + '.musicxml')
    score.write('musicxml', fp=xml_path)

    return xml_path
