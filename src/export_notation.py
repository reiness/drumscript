from music21 import converter, tempo, meter

def midi_to_musicxml(midi_path: str, xml_out: str, bpm: float = None, ts: str = '4/4'):
    score = converter.parse(midi_path)
    if bpm:
        mm = tempo.MetronomeMark(number=bpm)
        score.insert(0, mm)
    score.insert(0, meter.TimeSignature(ts))
    score.write('musicxml', fp=xml_out)
    return xml_out
