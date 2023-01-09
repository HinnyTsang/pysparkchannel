"""
Script to regenerate the file structure base on the JSON file
"""
import json
import os
from typing import Dict, Union

File = str
Folder = Dict[str, File]
Folder = Dict[str, Union[File, Folder]]

JSON_STRING="""$JSON_STRING$"""
BASE_PATH="""dest"""

def decode_expression(expression):
    """Decode expression"""
    return expression \
        .replace('"""""', '"') \
        .replace("\n", "\\n") \
        .replace('""""', '"\\"\\"\\"') \
        .replace('"""', '\\"\\"\\"')

def reconstruct_modules(base_path: str = "", force: bool = True) -> None:
    """Reconstruct the modules from the json string"""
    if os.path.exists(base_path) and not force:
        raise FileExistsError(f"Directory Exist {base_path}.")

    os.makedirs(base_path, exist_ok=True)
    loaded_modules: Dict[str, Folder] = json.loads(decode_expression(JSON_STRING))
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
        with open(full_path, "w", encoding="utf-8") as file:
            file.write(contains)

    elif isinstance(contains, dict):
        print(f"Reconstructing folder {full_path}")
        os.makedirs(full_path, exist_ok=True)
        for sub_path, sub_items in contains.items():
            reconstruct_path(base_path, sub_path, sub_items, force)

    else:
        raise ValueError(f"Unknown file type {contains}")


def main():
    """Main function of this script"""

    reconstruct_modules(decode_expression(BASE_PATH))


if __name__ == "__main__":
    main()
