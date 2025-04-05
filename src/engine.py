# ---------------------------------------------------------------------------- #
# Engine Script
# 
# This script orchestrates the data processing pipeline, including:
# - Pre-processing text files into vector stores
# - Running inference to generate answers
# - Post-processing results to save them in a CSV format
# ---------------------------------------------------------------------------- #

from src.pre_process.process_text import read_txt_file  # Function to read and process text files
from src.pre_process.vector import create_vector_store, retrieve_vector_store  # Vector store operations
from src.inference.chain import ask_gpt  # Function to query GPT model
from src.post_process.store_results import save_to_csv  # Function to save results to CSV
from src.pre_process.process_text import get_file_name  # Utility to extract file names
import os  # Operating system interface for file operations

# Define paths for data input and results output
DATA_PATH = "data/"
RESULTS_PATH = "results/"

def pre_process_vector_store():
    """
    Pre-process text files to create vector stores.
    
    This function walks through the DATA_PATH directory, reads each text file,
    and creates a vector store for each file's content.
    """
    for root, dirs, files in os.walk(DATA_PATH):
        for file in files:
            file_path = os.path.join(root, file)
            chunks, filename = read_txt_file(file_path)  # Read and split the file into chunks
            create_vector_store(filename, chunks)  # Create a vector store from the chunks
            print("Created vector store: ", file_path)  # Confirm vector store creation

def post_process_results():
    """
    Post-process results by querying the vector store and saving answers.
    
    This function retrieves vector stores, queries them using GPT, and saves
    the results to a CSV file.
    """
    for root, dirs, files in os.walk(DATA_PATH):
        for file in files:
            file_path = os.path.join(root, file)
            vector_store = retrieve_vector_store(get_file_name(file_path))  # Load the vector store
            answer = ask_gpt(vector_store)  # Query the vector store with GPT
            save_to_csv(answer, RESULTS_PATH + "military_casualties.csv")  # Save the answer to CSV
            print("Saved to csv: ", file_path)  # Confirm CSV save

def main():
    """
    Main function to execute the data processing pipeline.
    
    It runs the pre-processing and post-processing functions in sequence.
    """
    pre_process_vector_store()  # Step 1: Create vector stores from text files
    post_process_results()  # Step 2: Query vector stores and save results

if __name__ == "__main__":
    main()