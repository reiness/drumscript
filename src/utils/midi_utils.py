# utils/midi_utils.py

# Extend note map for melodic instruments too
note_map = {
    'KICK': 36,            # Kick drum
    'SNARE': 38,           # Snare drum
    'HIHAT': 42,           # Closed Hi-hat
    'PIANO_C4': 60,        # Middle C (Piano)
    'PIANO_E4': 64,        # E4 (Piano)
    'GUITAR_E3': 52,       # E3 (Guitar)
    'BASS_A1': 33,         # A1 (Bass guitar)
    'VIOLIN_A4': 69,       # A4 (Violin)
    'GUITAR_A3': 57,       # A3 (Guitar)
    'PIANO_G4': 67,        # G4 (Piano)
    # Add more notes as needed
}

# MIDI program numbers for General MIDI instruments
instrument_programs = {
    'PIANO': 0,            # Acoustic Grand Piano
    'GUITAR': 24,          # Acoustic Guitar (Nylon)
    'BASS': 32,            # Electric Bass (finger)
    'VIOLIN': 40,          # Violin
    'FLUTE': 73,           # Flute
    'TRUMPET': 56,         # Trumpet
    'SAX': 65,             # Alto Sax
    'DRUM': 0,             # Percussion instruments (is_drum=True, program number doesn't matter)
}

