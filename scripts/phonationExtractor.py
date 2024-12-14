import os
from timeit import default_timer as timer
from disvoice.phonation import Phonation
import concurrent.futures

n_processes = 8


def extract_phonation_features(audio_file):
    phonation = Phonation()
    static_features1 = phonation.extract_features_file(
        audio_file, static=False, plots=False, fmt="npy"
    )
    print(f"fileName: {audio_file}\t features: {static_features1}")
    return static_features1


def process_audio(audioFolder, outputFolder):
    os.makedirs(outputFolder, exist_ok=True)

    # extract_phonation_features("../AssameseAudios/Audios/seperateFiles/AA05_S1.wav")
    # return
    # for audioFile in os.listdir(audioFolder):
    #     if audioFile.endswith(".wav"):
    #         base_name = os.path.splitext(audioFile)[0]
    #         audio_path = os.path.join(audioFolder, audioFile)
    #         extract_glottal_features(
    #             "../AssameseAudios/Audios/seperateFiles/AA05_S1.wav"
    #         )

    # audio_files = os.listdir(audioFolder)
    audio_files = sorted(
        os.listdir(audioFolder),
        key=lambda f: os.path.getsize(os.path.join(audioFolder, f)),
    )
    for i in range(0, len(audio_files), n_processes):
        # for i in range(0, 2, n_processes):
        input_folders = []
        for j in range(0, 8):
            input_folders.append(os.path.join(audioFolder, audio_files[i + j]))
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=n_processes
        ) as executor:
            print(input_folders)
            results = list(executor.map(extract_phonation_features, input_folders))
            print(results)


if __name__ == "__main__":
    textGridFolder = "../Annotations"
    audioFolder = "../AssameseAudios/Audios/seperateFiles"
    outputFolder = "../Data/phonation_features"
    process_audio(audioFolder, outputFolder)
