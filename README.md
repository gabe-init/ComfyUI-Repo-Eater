# ComfyUI-Repo-Eater

A ComfyUI custom node that ingests GitHub repositories and outputs their content as text along with token count.

## Features

- Takes a GitHub repository URL as input
- Uses the gitingest library to download and process the repository
- Saves the full content as a .txt file in the ComfyUI output directory
- Outputs the raw text as a string for use in other ComfyUI nodes
- Counts and outputs the number of tokens in the repository content using tiktoken

## Installation

1. Clone this repository into your ComfyUI custom_nodes directory:
   ```
   cd ComfyUI/custom_nodes
   git clone https://github.com/yourusername/ComfyUI-Repo-Eater.git
   ```

2. Install the required dependencies:
   ```
   cd ComfyUI-Repo-Eater
   pip install -r requirements.txt
   ```

## Usage

1. Add the "GitHub Repo Eater" node to your workflow
2. Enter a GitHub repository URL in the "repo_url" field
3. Connect the outputs to other nodes that accept text input or use the token count

## Example

Input:
- repo_url: https://github.com/username/repository

Output:
- repo_content: A string containing the full content of the repository
- token_count: A string representing the number of tokens in the repository content (using GPT-3.5-Turbo tokenizer), formatted with commas for better readability (e.g., "155,779")
- A text file saved to the ComfyUI output directory (repo_eater folder)

## License

MIT# Trigger workflow
