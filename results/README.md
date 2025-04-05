# MIC Processing and Analysis Pipeline

This project provides a comprehensive pipeline for processing text files, transforming them into vector stores, running inference to generate answers, and post-processing results into a CSV format. It is designed to handle specific file formats and patterns, extracting Militarized Interstate Confrontations (MICs) metadata such as country codes and publication dates.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Modules](#modules)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Pre-Processing**: Read and process text files into vector stores.
- **Inference**: Query vector stores using a GPT model to generate answers.
- **Post-Processing**: Save results in a CSV format for further analysis.
- **Metadata Extraction**: Extracts country codes and publication dates from specific file formats.

## Installation

To use this project, ensure you have Python installed on your system. Clone the repository and install the necessary dependencies using the following commands:

```bash
git clone <repository-url>
cd <repository-directory>
pip install -r requirements.txt
```

## Usage

The main script for executing the data processing pipeline is `engine.py`. This script orchestrates the entire process, from pre-processing to post-processing.

```bash
python engine.py
```

### Example

To process text files and generate results, simply run the `engine.py` script. Ensure your data files are located in the `data/` directory.

## Modules

### Pre-Process

- **`process_text.py`**: Contains functions to read text files, split their contents into chunks, and extract metadata.
- **`vector.py`**: Handles vector store operations, including creation and retrieval.

### Inference

- **`chain.py`**: Provides functionality to query the GPT model.

### Post-Process

- **`store_results.py`**: Contains functions to save results to a CSV file.

## Dependencies

- `re`: Regular expressions for pattern matching.
- `langchain.text_splitter`: Utility for splitting text into chunks.
- `os`: Operating system interface for file operations.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or issues, please contact [Your Name] at [Your Email].
