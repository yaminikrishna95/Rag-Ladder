import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader


load_dotenv()  # Load environment variables from .env file




def  load_text_file():
    """
    Load a text file from the specified path.

    Returns:
        str: The content of the text file.
    """
    # Get the path to the text file from environment variable
    text_file_path = os.getenv("TEXT_FILE_PATH")
    
    if not text_file_path:
        raise ValueError("TEXT_FILE_PATH environment variable is not set.")
    
    # Create a Path object
    path = Path(text_file_path)
    
    if not path.is_file():
        raise FileNotFoundError(f"The file {text_file_path} does not exist.")
    
    # Load the text file using TextLoader
    loader = TextLoader(str(path))
    documents = loader.load()
    print(f"Loaded {len(documents)} documents from {text_file_path}.")
    print(f"content preview: {documents[0].page_content[:100]}...")  # Print a preview of the first document
    print(f"metadata: {documents[0].metadata}")  # Print metadata of the first document
    
    return documents