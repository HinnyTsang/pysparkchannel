"""
Script to rebuild the filestructure from the given binary string
"""
import json
import os
from typing import Dict, Iterable, Union

File = str
Folder = Dict[str, Union[File, Iterable["Folder"]]]

JSON_FILE="parsed_modules.json"
BASE_PATH="test"

text_ext_support = ['.py', '.txt', '.csv', '.ipynb']
binary_ext_support = ['.xlsx']

def decode_string(string: str) -> str:
    """
    Decode ord string to original string
    """
    str_to_ord_list = string.split(" ")

    if len(str_to_ord_list) == 0:
        return ""

    decoded_str = "".join(chr(int(s)) if len(s) > 0 else "" for s in str_to_ord_list)
    return decoded_str

def decode_binary_string(string: str) -> bytes:
    """
    Decode ord string to origin al string
    """
    return bytearray(map(int, string.split(" ")))

def reconstruct_modules(json_file: str = "", base_path: str="", force: bool = True) -> None:
    """Reconstruct the modules from the json string"""

    with open(json_file, "r", encoding="utf-8") as file:
        parsed_modules = file.read()

    loaded_modules: Dict[str, Folder] = json.loads(parsed_modules)

    for path, contains in loaded_modules.items():
        reconstruct_path(base_path, path, contains, force)

def reconstruct_path(
        base_path: str,
        path: str,
        contains: Union[File, Folder],
        force: bool
    ) -> None:
    """Reconstruct the modules from the json string"""
    full_path = os.path.join(base_path, path)
    if os.path.exists(full_path) and not force:
        raise FileExistsError(f"Directory Exist {full_path}.")

    if isinstance(contains, str):
        print(f"Reconstructing file {full_path}")

        _, file_extension = os.path.splitext(full_path)

        if file_extension in text_ext_support:
            # Read text file
            with open(full_path, "w", encoding="utf-8") as file:
                file.write(decode_string(contains))

        elif file_extension in binary_ext_support:
            # Read binary files
            with open(full_path, "wb") as file:
                file.write(decode_binary_string(contains))
        else:
            raise NotImplementedError(
                f"File extension '{file_extension}' are currently not supported"
            )


    elif isinstance(contains, dict):
        print(f"Reconstructing folder {full_path}")
        os.makedirs(full_path, exist_ok=True)
        for sub_path, sub_items in contains.items():
            reconstruct_path(base_path, sub_path, sub_items, force)

    else:
        raise ValueError(f"Unknown file type {contains}")


def main():
    """Main function of this script"""
    reconstruct_modules(JSON_FILE, BASE_PATH, True)

if __name__ == "__main__":
    main()
