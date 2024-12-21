import os
import numpy as np
from timeit import default_timer as timer
from disvoice.phonological import Phonological
import pandas as pd

# Log file to record errors
log_file_path = "error_log.txt"


def log_error(error_message):
    """Log the error message into the log file."""
    with open(log_file_path, "a") as log_file:
        log_file.write(error_message + "\n")


def extract_features(audio_file, output_folder):
    start_time = timer()  # Start timer for the file processing

    try:
        phonationf = Phonological()
        static_features1 = phonationf.extract_features_file(
            audio_file, static=True, plots=False, fmt="dataframe"
        )
        # print(f"Processing file: {audio_file}")

        # Save features to CSV
        base_name = os.path.basename(audio_file)
        file_name, _ = os.path.splitext(base_name)
        csv_file_path = os.path.join(output_folder, f"{file_name}.csv")

        static_features1.to_csv(csv_file_path, index=False)  # Use Pandas to save

    except Exception as e:
        error_message = f"Error processing file {audio_file}: {str(e)}"
        print(error_message)
        log_error(error_message)
        return (
            None,
            0,
        )  # Return None for the file path and 0 for elapsed time if there's an error

    end_time = timer()  # End timer for the file processing
    elapsed_time = end_time - start_time  # Time taken to process the file
    return (
        csv_file_path,
        elapsed_time,
    )  # Return the file path and the time taken for processing


def process_audio(audioFolder, outputFolder):
    os.makedirs(outputFolder, exist_ok=True)

    audio_files = sorted(
        os.listdir(audioFolder),
        key=lambda f: os.path.getsize(os.path.join(audioFolder, f)),
    )

    input_folders = [
        os.path.join(audioFolder, file)
        for file in audio_files
        if not os.path.exists(
            os.path.join(outputFolder, f"{os.path.splitext(file)[0]}.csv")
        )
    ]
    print(f"files left: {len(input_folders)}")

    total_start_time = timer()  # Start timer for the whole batch processing
    total_time_taken = 0
    total_files = 0
    failed_files = 0  # Count of failed files

    for audio_file in input_folders:
        result, elapsed_time = extract_features(audio_file, outputFolder)
        print(f"Donefile: {audio_file}\n\tElapsedTime: {elapsed_time}")

        if result is not None:
            total_time_taken += elapsed_time
            total_files += 1
        else:
            failed_files += 1  # Increment failed files count

    total_end_time = timer()  # End timer for the whole batch processing
    total_elapsed_time = total_end_time - total_start_time
    print(f"\n\n\nTotal execution time: {total_elapsed_time:.2f} seconds")
    if total_files > 0:
        average_time_per_file = total_time_taken / total_files
        print(f"Average execution time per file: {average_time_per_file:.2f} seconds")
    else:
        print("No files processed.")

    if failed_files > 0:
        print(
            f"\n{failed_files} files failed during processing. Check the log for details."
        )


if __name__ == "__main__":
    textGridFolder = "../Annotations"
    audioFolder = "/home/udayan/AaFiles/Speech/SpeakerIdentification-Assamese/AssameseAudios/Audios/seperateFiles/"
    outputFolder = "../Data/phonological_features/"
    process_audio(audioFolder, outputFolder)
