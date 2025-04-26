import os
import sys
import yaml
from cnnClassifier import logger
import json
import joblib
from box.exceptions import BoxValueError
from box import ConfigBox
from pathlib import Path
from typing import Any
from ensure import ensure_annotations
import base64


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Reads a YAML file and returns its content as a ConfigBox object.

    Args:
        path_to_yaml (Path): The path to the YAML file.

    Raises:
        ValueError: If the YAML file is empty.
        e: Any other exception that might occur while loading the YAML file.

    Returns:
        ConfigBox: The content of the YAML file as a ConfigBox object.
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"YAML file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("YAML file is empty.")
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """Creates a list of directories if they don't exist.

    Args:
        path_to_directories (list): List of paths to the directories to create.
        verbose (bool, optional): If True, logs a message after creating each directory. Defaults to True.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)  # Create the directory if it doesn't exist
        if verbose:
            logger.info(f"Created directory at: {path}")


@ensure_annotations
def save_json(path: Path, data: dict):
    """Saves a dictionary to a JSON file.

    Args:
        path (Path): Path where the JSON file will be saved.
        data (dict): The data to be saved in the JSON file.
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)  # Save the data as JSON with an indentation of 4 spaces
    logger.info(f"JSON file saved at: {path}")


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """Loads data from a JSON file and returns it as a ConfigBox object.

    Args:
        path (Path): Path to the JSON file.

    Returns:
        ConfigBox: The loaded data from the JSON file as a ConfigBox object.
    """
    with open(path) as f:
        content = json.load(f)
    logger.info(f"JSON file loaded successfully from: {path}")
    return ConfigBox(content)


@ensure_annotations
def save_bin(data: Any, path: Path):
    """Saves data to a binary file.

    Args:
        data (Any): The data to be saved as binary.
        path (Path): Path where the binary file will be saved.
    """
    joblib.dump(value=data, filename=path)  # Save the data as a binary file
    logger.info(f"Binary file saved at: {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    """Loads data from a binary file.

    Args:
        path (Path): Path to the binary file.

    Returns:
        Any: The data loaded from the binary file.
    """
    data = joblib.load(path)  # Load the binary data from the file
    logger.info(f"Binary file loaded from: {path}")
    return data


@ensure_annotations
def get_size(path: Path) -> str:
    """Returns the size of a file in KB.

    Args:
        path (Path): Path to the file.

    Returns:
        str: The size of the file in KB.
    """
    size_in_kb = round(os.path.getsize(path) / 1024)  # Calculate file size in KB
    return f"~ {size_in_kb} KB"


def decodeImage(imgstring, fileName):
    """Decodes a base64 string into an image and saves it to a file.

    Args:
        imgstring (str): The base64 encoded image string.
        fileName (str): The file path where the image will be saved.
    """
    imgdata = base64.b64decode(imgstring)  # Decode the base64 string into binary data
    with open(fileName, 'wb') as f:
        f.write(imgdata)  # Save the binary data to the file
        f.close()


def encodeImageIntoBase64(croppedImagePath):
    """Encodes an image into a base64 string.

    Args:
        croppedImagePath (str): Path to the image file.

    Returns:
        str: The base64 encoded string of the image.
    """
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())  # Read the image and encode it into base64