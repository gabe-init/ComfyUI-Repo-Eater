import os
import json
import time
from pathlib import Path
from gitingest import ingest
import tiktoken

# Import ComfyUI's folder_paths module to get the correct output directory
import folder_paths

class RepoEaterNode:
    """
    A node that ingests a GitHub repository and outputs its content as a string.
    
    This node:
    1. Takes a GitHub repository URL as input
    2. Uses gitingest to download and process the repository
    3. Saves the full content as a .txt file
    4. Outputs the raw text as a string and token count
    """
    
    def __init__(self):
        # Create output directory if it doesn't exist
        self.output_dir = Path(os.path.join(folder_paths.get_output_directory(), "repo_eater"))
        os.makedirs(self.output_dir, exist_ok=True)
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "repo_url": ("STRING", {
                    "multiline": False,
                    "default": "https://github.com/username/repository"
                }),
            },
        }
    
    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("repo_content", "token_count",)
    FUNCTION = "ingest_repo"
    CATEGORY = "utils"
    
    def count_tokens(self, text, model="gpt-3.5-turbo"):
        """
        Count the number of tokens in a text string using tiktoken.
        
        Args:
            text (str): The text to count tokens for
            model (str): The model to use for token counting
            
        Returns:
            int: The number of tokens in the text
        """
        try:
            # Initialize the encoder for the specified model
            encoding = tiktoken.encoding_for_model(model)
            
            # Count tokens
            tokens = encoding.encode(text, disallowed_special=())
            return len(tokens)
        except Exception as e:
            print(f"Error counting tokens: {str(e)}")
            # Fallback to a simple approximation if tiktoken fails
            return len(text.split())
    
    def ingest_repo(self, repo_url):
        """
        Ingest a GitHub repository and return its content as a string.
        
        Args:
            repo_url (str): URL of the GitHub repository
            
        Returns:
            tuple: (repo_content, token_count)
        """
        try:
            # Use gitingest to download and process the repository
            summary, tree, content = ingest(repo_url)
            
            # Create a timestamp for the filename
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            
            # Extract repo name from URL for the filename
            repo_name = repo_url.rstrip('/').split('/')[-1]
            output_filename = f"{repo_name}.txt"
                
            # Add timestamp to filename to avoid overwriting
            filename = f"{timestamp}_{output_filename}"
            output_path = self.output_dir / filename
            
            # Save the content to a file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"Repository content saved to {output_path}")
            
            # Count tokens in the content
            token_count = self.count_tokens(content)
            
            # Format token count with commas for better readability
            formatted_token_count = f"{token_count:,}"
            
            # Return the content as a string and the formatted token count as a string
            return (content, formatted_token_count)
            
        except Exception as e:
            error_message = f"Error ingesting repository: {str(e)}"
            print(error_message)
            return (error_message, "0")  # Zero doesn't need comma formatting
    
    @classmethod
    def IS_CHANGED(cls, repo_url):
        """
        This method ensures the node is re-executed when the inputs change.
        """
        return repo_url

# Node class mappings
NODE_CLASS_MAPPINGS = {
    "RepoEaterNode": RepoEaterNode
}

# Node display name mappings
NODE_DISPLAY_NAME_MAPPINGS = {
    "RepoEaterNode": "GitHub Repo Eater"
}