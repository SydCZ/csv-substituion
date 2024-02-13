"""
substitue.py

Description: Used for substitute or anonymize data
Author: Michal Panek

MIT License
Copyright (c) 2024 Michal Panek
"""

# /home/mpanek/git/csv-substituion/test-data/WG/Anonymization-memcon1.csv

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
                print(f"Original number: {original}, New number: {new}")
                directory_to_search = "/home/mpanek/git/csv-substituion/test-data/WG"
                search_term = str(original)
                found_files = search_files(directory_to_search, search_term)
                print("Found files:")
                for file_path in found_files:
                    print(file_path)

if __name__ == "__main__":
    main()
