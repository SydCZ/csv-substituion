"""
substitute.py

Description: Used for substitute or anonymize data
Author: Michal Panek

MIT License
Copyright (c) 2024 Michal Panek
"""

import csv
import os
import sys

def process_anonymization_pair(numbers):
    # Check if both numbers are valid integers and skip headers on malformed data
    if not (numbers[0].strip().isdigit() and numbers[1].strip().isdigit()):
        # If either number is not a valid integer, skip processing this line
        print("Skipping line as it does not contain valid integers:", numbers)
        return False
    else : 
        original = int(numbers[0])
        new = int(numbers[1])
        return original, new
    
def search_files(directory, search_term):
    found_files = []

    # Walk through the directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file has a .csv suffix
            if file.lower().endswith('.csv'):
                # Check if the search term is in the file name (case insensitive)
                if search_term.lower() in file.lower():
                    # If found, add the file's full path to the list of found files
                    found_files.append(os.path.join(root, file))

    return found_files


def is_valid_file_path(file_path):
    return os.path.isfile(file_path)

def get_directory_from_file_path(file_path):
    # Extract the directory path from the file path
    directory_path = os.path.dirname(file_path)
    print("Directory path:", directory_path)
    return directory_path

def substitute_values_in_csv(csv_file_path, original_number, new_number, column):
    # Create a temporary file to write the updated contents
    temp_file_path = csv_file_path + '.tmp'

    # Open the original CSV file for reading and the temporary file for writing
    with open(csv_file_path, 'r', newline='') as input_file, \
            open(temp_file_path, 'w', newline='') as output_file:

        reader = csv.reader(input_file)
        writer = csv.writer(output_file)

        # Get the header row
        header = next(reader)
        header_length = len(header)
        try:
            column_index = header.index(column)
        except ValueError:
            print(f"Column '{column}' not found in the CSV file.")
            return

        # Write the header row to the temporary file
        writer.writerow(header)

        # Iterate over each row in the CSV file
        for row in reader:
            # Check if the specified column exists and contains the original value
            if column_index < header_length:
                value = row[column_index]
                # Perform string replacement
                row[column_index] = value.replace(str(original_number), str(new_number))

            # Write the updated row to the temporary file
            writer.writerow(row)

    # Rename the temporary file
    os.replace(temp_file_path, csv_file_path)

def extract_number_from_path(path):
    # Extract the numbers from the path using a regular expression
    # This assumes that the number is the last part of the path before the file extension
    import re
    match = re.search(r'\d+(?=\.[^.]*$)', path)
    if match:
        return match.group(0)
    else:
        return None

def main():
    # Ask user to input the path to the CSV file
    csv_file_path = input("Enter the path to the CSV with anonymization pairs file: ").strip()

    if not is_valid_file_path(csv_file_path):
        print("The provided path is not a valid path to a file.")
        sys.exit(1)
    else:
        directory_to_search = get_directory_from_file_path(csv_file_path)

    print("Directory to search:", directory_to_search)

    # Open the CSV file
    with open(csv_file_path, 'r') as file:
        # Create a CSV reader object
        reader = csv.reader(file)
        
        # Iterate over each line in the CSV file
        for line in reader:
            # Process each line
            if process_anonymization_pair(line):
                original, new = process_anonymization_pair(line)
                search_term = str(original)
                found_files = search_files(directory_to_search, search_term)
                print("-" * 15)
                print(f"Original number: {original}, new number: {new}")
                print("Found files:")
                for file_path in found_files:
                    print(file_path)
                    print()
                    print(f"Editing files {original} -> {new}")
                    substitute_values_in_csv(file_path, original, new, "logfile")
                    substitute_values_in_csv(file_path, original, new, "subject_nr")
                    anonymized_file_name = file_path.replace(str(original), str(new) + "_anonymized")
                    print(f"Renaming original {file_path} to {anonymized_file_name}")
                    os.replace(file_path, anonymized_file_name)

if __name__ == "__main__":
    main()
