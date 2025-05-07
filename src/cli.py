import os
import click
from pathlib import Path
import time
from src.separate_drums import isolate_drums
from src.transcribe_drums import transcribe
from src.build_midi import events_to_midi
from src.build_musicxml import midi_to_musicxml

@click.command()
@click.argument('input', type=click.Path(exists=True))
@click.option('--out', default='results/', help='Output directory.')
def main(input, out):
    try:
        print(f"\n🎧 Input audio: {input}")
        os.makedirs(out, exist_ok=True)

        # Step 1: Isolate drums
        print("🥁 Step 1: Isolating drums...")
        isolate_drums(input, out)

        drum_path = Path(out) / Path(input).stem / "drums.wav"
        drum_path = drum_path.resolve()
        input_name = Path(input).stem 

        # Wait for file to exist
        max_wait = 60  # seconds
        waited = 0
        while not drum_path.exists():
            if waited >= max_wait:
                raise FileNotFoundError(f"Timed out waiting for {drum_path}")
            time.sleep(0.5)
            waited += 0.5

        print(f"✅ Drums extracted → {drum_path}")

        # Step 2: Transcribe drum hits
        print("🧠 Step 2: Transcribing drum hits...")
        events = transcribe(drum_path)
        if not events:
            print("⚠️ No drum events detected!")
        else:
            print(f"✅ Detected {len(events)} drum hits")

        # Step 3: Build MIDI
        print("🎼 Step 3: Building MIDI...")
        midi_path = events_to_midi(events, out, input_name)
        print(f"✅ MIDI saved → {midi_path}")

        # Step 4 (Optional): Convert to MusicXML
        if os.path.exists(midi_path):
            print("📄 Step 4: Converting to MusicXML...")
            xml_path = midi_to_musicxml(midi_path, out, input_name)  
            print(f"✅ MusicXML saved → {xml_path}")

        print("\n🎉 Done!")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    main()
