import json
import re
import logging
from datetime import datetime

# Set up a logger for reusable logging functionality
logger = logging.getLogger("AI-Agents")
logger.setLevel(logging.INFO)

# Create a console handler and set the level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)

def clean_text(text):
    """
    Cleans a given text by removing special characters, extra spaces, and converting to lowercase.

    Args:
        text (str): The text to clean.

    Returns:
        str: The cleaned text.
    """
    if not isinstance(text, str):
        return text
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    return text.strip().lower()

def save_to_json(data, filename):
    """
    Saves a Python dictionary or list to a JSON file.

    Args:
        data (dict or list): The data to save.
        filename (str): The path to the JSON file.

    Returns:
        None
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        logger.info(f"Data successfully saved to {filename}")
    except Exception as e:
        logger.error(f"Failed to save data to {filename}: {e}")

def read_from_json(filename):
    """
    Reads data from a JSON file and returns it as a Python object.

    Args:
        filename (str): The path to the JSON file.

    Returns:
        dict or list: The loaded JSON data.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        logger.info(f"Data successfully loaded from {filename}")
        return data
    except Exception as e:
        logger.error(f"Failed to read data from {filename}: {e}")
        return None

def timestamp():
    """
    Returns the current timestamp in a readable format.

    Returns:
        str: The current timestamp in YYYY-MM-DD HH:MM:SS format.
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def chunk_list(input_list, chunk_size):
    """
    Splits a list into smaller chunks of a specified size.

    Args:
        input_list (list): The list to split.
        chunk_size (int): The size of each chunk.

    Returns:
        list of lists: A list containing smaller chunks of the input list.
    """
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]

def validate_url(url):
    """
    Validates if a given string is a properly formatted URL.

    Args:
        url (str): The URL to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    pattern = re.compile(
        r'^(https?:\/\/)?'  # http:// or https://
        r'([a-zA-Z0-9-_]+\.)+[a-zA-Z]{2,}'  # domain
        r'(:[0-9]{1,5})?(\/[^\s]*)?$'  # optional port and path
    )
    return re.match(pattern, url) is not None
