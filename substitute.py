import pandas as pd
import os

# Function to read the mapping file, ie containing the anonymization pairs
def read_mapping_file(mapping_file_path):
    mapping_df = pd.read_csv(mapping_file_path, sep=';', header=None)
    mapping_df.columns = ['original', 'replacement']
    return mapping_df

# Function to process each CSV file that requires anonymization
def process_csv_file(csv_file_path, mapping_df):
    df = pd.read_csv(csv_file_path)
    # TODO Multiple columns possible, search for all columns that contains the original value and check for user input if needed
    df['first_column'] = df['first_column'].apply(lambda x: mapping_df.loc[mapping_df['original'] == x, 'replacement'].values[0] if x in mapping_df['original'].values else x)
    return df

# Function to process all CSV files in a directory
def process_all_csv_files(input_directory, output_directory, mapping_df):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    for filename in os.listdir(input_directory):
        if filename.endswith(".csv"):
            input_file_path = os.path.join(input_directory, filename)
            output_file_path = os.path.join(output_directory, filename)
            df = process_csv_file(input_file_path, mapping_df)
            df.to_csv(output_file_path, index=False)

# Paths
mapping_file_path = 'mapping.csv'  # Path to your mapping file
input_directory = 'input_csv_files'  # Directory containing input CSV files
output_directory = 'output_csv_files'  # Directory where modified CSV files will be saved

# Read mapping file
mapping_df = read_mapping_file(mapping_file_path)

# Process all CSV files
process_all_csv_files(input_directory, output_directory, mapping_df)
