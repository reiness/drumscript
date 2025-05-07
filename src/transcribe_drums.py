import numpy as np
from madmom.features.onsets import CNNOnsetProcessor, OnsetPeakPickingProcessor

def transcribe(audio_path):
    print("🔍 Loading audio and extracting onset probabilities...")
    proc = CNNOnsetProcessor()
    act = proc(audio_path)

    print("📈 Performing peak picking...")
    peak_picker = OnsetPeakPickingProcessor(threshold=0.3, fps=100)
    onsets = peak_picker(act)

    if len(onsets) == 0:
        print("⚠️ No onsets detected.")
        return []

    print(f"✅ Found {len(onsets)} onsets.")

    # Temporary mapping: each onset mapped to all drums (for simulation)
    events = []
    for t in onsets:
        events.append((t, ['KICK', 'SNARE', 'HIHAT']))

    return events
