from pydub import AudioSegment, silence
import os


def annotate_audio_to_textgrid(
    file_path,
    silence_thresh=-50,
    min_silence_len=10,
    output_dir="output_segments",
    textgrid_file="output.TextGrid",
):
    """
    Annotates an audio file by splitting it into segments based on silence and outputs a TextGrid file.

    Args:
        file_path (str): Path to the audio file.
        silence_thresh (int): Silence threshold in dBFS.
        min_silence_len (int): Minimum length of silence in ms to consider as a segment break.
        output_dir (str): Directory to save the audio segments.
        textgrid_file (str): Path to save the TextGrid file.

    Returns:
        None
    """
    # Load the audio file
    audio = AudioSegment.from_file(file_path)

    # Detect silent parts
    silent_ranges = silence.detect_silence(
        audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh
    )
    silent_ranges = [(start, end) for start, end in silent_ranges]

    # Convert silence ranges into segments
    segments = []
    start = 0
    for silence_start, silence_end in silent_ranges:
        segments.append((start, silence_start))
        start = silence_end
    segments.append((start, len(audio)))  # Add the last segment

    # Write TextGrid file
    with open(textgrid_file, "w") as tg:
        tg.write('File type = "ooTextFile"\n')
        tg.write('Object class = "TextGrid"\n\n')
        tg.write(f"xmin = 0\n")
        tg.write(f"xmax = {len(audio) / 1000}\n")  # Total duration in seconds
        tg.write("tiers? <exists>\nsize = 1\n")
        tg.write("item []:\n")
        tg.write("    item [1]:\n")
        tg.write('        class = "IntervalTier"\n')
        tg.write('        name = "Annotation"\n')
        tg.write(f"        xmin = 0\n")
        tg.write(f"        xmax = {len(audio) / 1000}\n")
        tg.write(f"        intervals: size = {len(segments)}\n")

        for i, (start, end) in enumerate(segments):
            tg.write(f"        intervals [{i + 1}]:\n")
            tg.write(f"            xmin = {start / 1000}\n")  # Start time in seconds
            tg.write(f"            xmax = {end / 1000}\n")  # End time in seconds
            tg.write(f'            text = "Segment {i + 1}"\n')


if __name__ == "__main__":
    # Path to the audio file
    audio_file = "AA10.wav"  # Replace with your file path

    # Call the function
    annotate_audio_to_textgrid(
        file_path=audio_file,
        silence_thresh=-50,  # Adjust as needed
        min_silence_len=100,  # Minimum silence in milliseconds
        textgrid_file="AA10.TextGrid",  # Output TextGrid file
    )

    print("Annotation completed. Check 'AA10.TextGrid' for the TextGrid file.")
