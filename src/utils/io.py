import json
from typing import Union
from pathlib import Path

def read_json(file_path):
    """Reads the json file and returns the dict

    Args:
        file_path (Union[str, Path]): file path of the json file
    """
    with open(file_path) as f:
        return json.load(f)

def read_file(file_path: Union[str, Path]):
    """Reads a file and returns the content

    Args:
        file_path (Union[str, Path]): file path of the file
    """
    with open(file_path) as f:
        return f.read()
