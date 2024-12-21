import os
from textgrid import TextGrid
from pydub import AudioSegment


def extract_segments_from_textgrid(textgrid_path, audio_path, output_folder):
    # Load the TextGrid file
    tg = TextGrid.fromFile(textgrid_path)
    tiers = tg.tiers

    # Load the audio file
    audio = AudioSegment.from_file(audio_path)

    # Resample the audio to 16 kHz
    audio = audio.set_frame_rate(16000)

    # Get the base filename without extension
    base_name = os.path.splitext(os.path.basename(audio_path))[0]

    segment_count = 0
    # Iterate over tiers and intervals
    for tier in tiers:
        for interval in tier.intervals:
            start = int(interval.minTime * 1000)  # Convert to milliseconds
            end = int(interval.maxTime * 1000)  # Convert to milliseconds
            label = interval.mark.strip()  # Get the segment name/label

            if label:  # Skip empty labels
                # Extract the segment
                segment = audio[start:end]

                # Create output file name
                segment_filename = f"{base_name}_{label}.wav"
                output_path = os.path.join(output_folder, segment_filename)

                # Save the extracted segment
                segment.export(output_path, format="wav")
                segment_count += 1
                # print(f"Exported: {output_path}")
    return segment_count


def process_textgrid_and_audio_files(textgrid_folder, audio_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Process each TextGrid file in the folder
    for textgrid_file in os.listdir(textgrid_folder):
        if textgrid_file.endswith(".TextGrid"):
            base_name = os.path.splitext(textgrid_file)[0]
            textgrid_path = os.path.join(textgrid_folder, textgrid_file)

            # Find the corresponding audio file
            audio_path = os.path.join(audio_folder, f"{base_name}.wav")
            if os.path.exists(audio_path):
                segment_count = extract_segments_from_textgrid(
                    textgrid_path, audio_path, output_folder
                )
                print(f"{audio_path}: {segment_count} Segments")
            else:
                print(f"Audio file not found for: {base_name}")


if __name__ == "__main__":
    # Specify paths
    textgrid_folder = "../Annotations/"
    audio_folder = "../AssameseAudios/Audios/"
    output_folder = "../AssameseAudios/Audios/seperateFiles/"

    # Process files
    process_textgrid_and_audio_files(textgrid_folder, audio_folder, output_folder)
