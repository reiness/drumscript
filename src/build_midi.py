import os
import pretty_midi
from src.utils.midi_utils import note_map

def events_to_midi(events, out_dir: str, input_name: str):
    pm = pretty_midi.PrettyMIDI()

    # Create a separate instrument for each drum part
    instruments = {k: pretty_midi.Instrument(program=0, is_drum=True, name=k) for k in note_map}

    for t, voices in events:
        for v in voices:
            if v in note_map:
                pitch = note_map[v]
                instruments[v].notes.append(
                    pretty_midi.Note(velocity=100, pitch=pitch, start=t, end=t+0.05)
                )

    # Add each instrument to the MIDI
    for instr in instruments.values():
        pm.instruments.append(instr)

    # Ensure the output directory structure exists
    result_dir = os.path.join(out_dir, input_name)  # Create a subfolder with input_name
    os.makedirs(result_dir, exist_ok=True)
    
    # Construct the output path for the MIDI file
    midi_path = os.path.join(result_dir, "drums.mid")
    
    # Write the MIDI file to the desired path
    pm.write(midi_path)

    return midi_path
