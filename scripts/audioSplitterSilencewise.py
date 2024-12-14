import os
from textgrid import TextGrid
from pydub import AudioSegment
import parselmouth
from parselmouth.praat import call
import numpy as np
from pydub import AudioSegment
from pydub.silence import detect_silence


def detect_silences(audio_path, silence_threshold=-25, min_silence_duration=300):
    """
    Detects silences in a WAV file.

    Parameters:
        wav_file_path (str): Path to the WAV file.
        silence_thresh (int): Silence threshold in dBFS (default: -40 dBFS).
        min_silence_len (int): Minimum silence length in milliseconds (default: 1000 ms).

    Returns:
        list: A list of tuples where each tuple represents the start and end (in milliseconds) of a silence.
    """
    # Load the audio file
    audio = AudioSegment.from_wav(audio_path)

    # Detect silence
    silences = detect_silence(
        audio, min_silence_len=min_silence_duration, silence_thresh=silence_threshold
    )

    # Convert silence start and end times to seconds
    silences_in_seconds = [(start / 1000, end / 1000) for start, end in silences]

    return silences_in_seconds


# if __name__ == "__main__":
#     import argparse
#
#     parser = argparse.ArgumentParser(description="Detect silences in an audio file.")
#     parser.add_argument("audio_file", type=str, help="Path to the audio file.")
#     parser.add_argument(
#         "--threshold",
#         type=float,
#         default=-25,
#         help="Silence threshold in dB (default: -25).",
#     )
#     parser.add_argument(
#         "--min_duration",
#         type=float,
#         default=0.3,
#         help="Minimum silence duration in seconds (default: 0.3).",
#     )
#
#     args = parser.parse_args()
#
#     if not os.path.isfile(args.audio_file):
#         print(f"Error: File '{args.audio_file}' does not exist.")
#     else:
#         silences = detect_silences(args.audio_file, args.threshold, args.min_duration)
#         if silences:
#             print("Detected silences:")
#             for start, end in silences:
#                 print(f"- From {start:.2f} to {end:.2f} seconds")
#         else:
#             print("No silences detected.")


def extract_segments_from_textgrid(textgrid_path, audio_path, output_folder):
    silences = detect_silences(audio_path, 100, 500)

    if silences:
        print("Detected silences:")
        for i, (start, end) in enumerate(silences, 1):
            print(f"{i}. Start: {start:.2f}s, End: {end:.2f}s")
    else:
        print("No silences detected.")
    return
    # Load the TextGrid file
    tg = TextGrid.fromFile(textgrid_path)
    tiers = tg.tiers

    # Load the audio file
    audio = AudioSegment.from_file(audio_path)

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
