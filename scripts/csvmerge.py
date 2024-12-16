import os
import pandas as pd
import argparse


def merge_csv_files(input_directory, output_file):
    """
    Merges all CSV files in the specified directory into a single CSV file,
    adding an extra column to indicate the source filename.

    Parameters:
        input_directory (str): Path to the directory containing CSV files.
        output_file (str): Path to the output merged CSV file.
    """
    # List to hold dataframes
    dataframes = []

    # Iterate over files in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(input_directory, filename)

            # Read CSV into a DataFrame
            df = pd.read_csv(filepath)
            print(f"processed: {filename}")

            # Add a column with the filename (excluding extension) as the first column
            df.insert(0, "source_file", os.path.splitext(filename)[0])

            # Append the dataframe to the list
            dataframes.append(df)

    # Concatenate all dataframes
    merged_df = pd.concat(dataframes, ignore_index=True)

    # Save the merged dataframe to a new CSV file
    merged_df.to_csv(output_file, index=False)


# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Merge multiple CSV files into a single CSV file."
    )
    parser.add_argument(
        "input_directory", type=str, help="Path to the directory containing CSV files."
    )
    parser.add_argument(
        "output_file", type=str, help="Path to the output merged CSV file."
    )

    args = parser.parse_args()

    merge_csv_files(args.input_directory, args.output_file)
    print(f"Merged CSV saved to {args.output_file}")
