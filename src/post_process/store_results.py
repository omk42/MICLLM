# ---------------------------------------------------------------------------- #
# Post-Processing: Store Results
# 
# This module provides functionality to extract structured data from model
# responses and save it to a CSV file for further analysis or reporting.
# ---------------------------------------------------------------------------- #

import csv  # CSV file operations
import re  # Regular expressions for pattern matching
from pathlib import Path  # Path operations for file existence checks

def save_to_csv(model_response, filename: str = "results/military_casualties.csv"):
    """
    Append extracted data to a CSV file, creating headers if the file doesn't exist.
    
    Args:
        model_response: The structured response from the model.
        filename (str): The path to the CSV file where data will be saved.
    """
    data = extract_data(model_response)  # Extract data from the model response
    file_exists = Path(filename).exists()  # Check if the file already exists
    
    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Date", "Death Count", "Countries involved"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()  # Write headers if the file is new
            
        writer.writerows(data)  # Append the extracted data

def extract_data(model_response) -> list[dict]:
    """
    Extract structured data from the model's response.
    
    Args:
        model_response: The response from the model containing structured text.
        
    Returns:
        list[dict]: A list of dictionaries with extracted data fields.
    """
    # Extract the answer part of the response
    answer = model_response["result"]

    # Define a regex pattern to extract date, death count, and countries involved
    pattern = r"-\sDate:\s*(.+?)\n\s*-\sDeath\sCount:\s*(.+?)\n\s*-\sCountries\sinvolved:\s*(.+?)\n\n"
    matches = re.findall(pattern, answer, re.DOTALL)
    
    # Return the extracted data as a list of dictionaries
    return [
        {
            "Date": date.strip(), 
            "Death Count": death_count.strip(),
            "Countries involved": countries.strip()
        }
        for date, death_count, countries in matches
    ]

if __name__ == "__main__":
    # Example usage: Extract data from a sample response and save it
    response = "- Date: April 1 - Death Count: 1212\n- Date: April 2 - Death Count: 1313\n- Date: April 3 - Death Count: 1414\n- Date: April 4 - Death Count: 1515"
    sample_response = {
        "result":  "sample",
        "metadata": {
            "country_codes": "US, UK",
            "published_date": "2024-01-01"
        }
    }
    extracted_data = extract_data(sample_response)
    save_to_csv(extracted_data)
