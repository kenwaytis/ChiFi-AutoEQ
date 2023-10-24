import pandas as pd
import argparse

def main(args):
    # Read the CSV file
    df = pd.read_csv(args.input, header=None)

    # Identify all duplicate rows (excluding the first occurrence)
    duplicated_rows = df[df.duplicated(subset=df.columns[0], keep='first')]

    # Print the removed rows and the number of removed rows
    print("Removed rows:")
    print(duplicated_rows)
    print(f"A total of {len(duplicated_rows)} rows were removed.")

    # Keep only the first occurrence of duplicate rows based on the first column
    df.drop_duplicates(subset=df.columns[0], keep='first', inplace=True)

    # Save the result to a new CSV file
    df.to_csv(args.output, header=False, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Remove all but the first occurrence of duplicate rows in a CSV file based on the first column.')
    parser.add_argument('--input', '-i', type=str, required=True, help='Path to the input CSV file')
    parser.add_argument('--output', '-o', type=str, required=True, help='Path to the output CSV file')

    args = parser.parse_args()
    main(args)

