# ---------------------------------------------------------------------------- #
# Text Processing Utilities
# 
# This module provides functions to read text files, split their contents into
# manageable chunks, and extract metadata such as country codes and publication
# dates. It is designed to handle specific file formats and patterns.
# ---------------------------------------------------------------------------- #

import re  # Regular expressions for pattern matching
from langchain.text_splitter import RecursiveCharacterTextSplitter  # Utility for splitting text into chunks

def read_txt_file(file_path):
    """
    Reads a text file and returns its contents as chunks with metadata.
    
    Args:
        file_path (str): Path to the text file to be read.
        
    Returns:
        tuple: A list of chunks with metadata and the file name.
    """
    with open(file_path, 'r', encoding='latin-1') as file:
        content = file.read()
        # Check if the file is from a specific set of years
        if file.name in ["2002.txt", "2003.txt", "2004.txt", "2005.txt", "2006.txt", "2007.txt", "2008.txt", "2009.txt", "2010.txt", "2011.txt"]:
            # Use a specialized chunking function for these years
            return chunk_file_for_year_content(content), file.name
        else:
            # Use the general chunking function for other files
            return chunk_file_content(content), file.name

def get_file_name(file_path):
    """
    Extracts and returns the name of the file from the file path.
    
    Args:
        file_path (str): Path to the text file.
        
    Returns:
        str: The name of the file.
    """
    with open(file_path, 'r', encoding='latin-1') as file:
        return file.name

def chunk_file_for_year_content(content):
    """
    Splits file content into chunks based on a regex pattern and extracts metadata.
    
    This function is tailored for files from specific years, extracting country
    codes and publication dates from the content.
    
    Args:
        content (str): The full text content of the file.
        
    Returns:
        list: A list of dictionaries, each containing a text chunk and its metadata.
    """
    pattern = r'\n=+\n'  # Pattern to split sections in the file
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)  # Initialize text splitter
    
    # Split the content into sections
    sections = re.split(pattern, content)
    result = []  # List to hold chunks with metadata

    # Iterate through sections to extract metadata and split into chunks
    for i in range(2, len(sections), 2):
        chunk = sections[i].strip()  # Extract the text chunk
        codes = re.findall(r'([A-Z]+)-([A-Z]+)', sections[i - 1])  # Extract country codes
        
        pattern = r"\n\-+\n"  # Pattern to split news articles within a section
        news_articles = re.split(pattern, chunk)

        for article in news_articles:
            md_pattern = r"SVM score:.*\n"  # Pattern to split metadata from content
            content = re.split(md_pattern, article)
            
            # Pattern to find publication dates in the content
            date_pattern = r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,2},\s\d{4}(?:,*\s?)?(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b"
            published_date = re.search(date_pattern, content[0])
            if published_date:
                published_date = published_date[0]
            if len(codes) > 1:
                codes = codes[0]
            else:
                codes = None
        
            # Split the article content into smaller chunks
            chunks = splitter.split_text(content[1])
            for chunk in chunks:
                result.append({
                    'content': chunk, 
                    'country_codes': codes,
                    'published_date': published_date
                })

    return result

def chunk_file_content(content):
    """
    Splits file content into chunks without extracting metadata.
    
    This function is used for files that do not require metadata extraction.
    
    Args:
        content (str): The full text content of the file.
        
    Returns:
        list: A list of dictionaries, each containing a text chunk.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)  # Initialize text splitter
    pattern = r'\n\_+\n'  # Pattern to split sections in the file
    
    # Split the content into sections
    sections = re.split(pattern, content)
    result = []  # List to hold chunks

    # Split each section into smaller chunks
    for section in sections:
        chunks = splitter.split_text(section)
        for chunk in chunks:
            result.append({
                'content': chunk, 
                'country_codes': None,
                'published_date': None
            })
    return result

if __name__ == "__main__":
    # Example usage: Read and process a specific text file
    file_path = "data/ProQuestDocuments-2025-01-17-11.txt"
    chunks = read_txt_file(file_path)
    print(chunks[-1])  # Print the last chunk
    print(chunks[-2])  # Print the second to last chunk