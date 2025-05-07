import os
import pretty_midi
from src.utils.midi_utils import note_map, instrument_programs

def events_to_midi(events, out_dir: str, input_name: str):
    pm = pretty_midi.PrettyMIDI()

    instruments = {}

    for t, voices in events:
        for v in voices:
            if v not in note_map:
                continue
            pitch = note_map[v]

            # Determine if it's a drum (percussion), guitar, or piano
            is_drum = v.upper() in ['KICK', 'SNARE', 'HIHAT', 'TOM', 'CRASH', 'RIDE']
            is_guitar = v.upper() in ['GUITAR', 'BASS']
            is_piano = v.upper() in ['PIANO']

            # Use the part name to choose the instrument program
            name = v.upper().split('_')[0]

            if is_drum:
                program = instrument_programs.get('DRUM', 0)  # Program for drums (percussion)
            elif is_guitar:
                program = instrument_programs.get('GUITAR', 25)  # Acoustic Guitar (Nylon)
            elif is_piano:
                program = instrument_programs.get('PIANO', 0)  # Acoustic Grand Piano
            else:
                program = instrument_programs.get(name, 0)  # Default to Acoustic Grand Piano for others

            # Create an instrument for this part if it doesn't exist
            if v not in instruments:
                instruments[v] = pretty_midi.Instrument(
                    program=program, is_drum=is_drum, name=v
                )

            # Notes for drums have shorter durations, others are longer
            note_duration = 0.05 if is_drum else 0.5
            note = pretty_midi.Note(
                velocity=100,
                pitch=pitch,
                start=t,
                end=t + note_duration
            )
            instruments[v].notes.append(note)

    # Add all instruments (drums, guitar, piano, etc.) to the PrettyMIDI object
    for instr in instruments.values():
        pm.instruments.append(instr)

    # Ensure the output directory structure exists
    result_dir = os.path.join(out_dir, input_name)
    os.makedirs(result_dir, exist_ok=True)

    # Write the MIDI file
    midi_path = os.path.join(result_dir, "instruments.mid")
    pm.write(midi_path)

    return midi_path
