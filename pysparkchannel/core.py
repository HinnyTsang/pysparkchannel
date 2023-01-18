"""Module Parser

Parse a module into a text files.
"""
import glob
import json
import os
from typing import Dict, Iterable, Union
from pysparkchannel.utils import fluent, encode_string, encode_binary_string

parser_ignore = ["__pycache__", "pysparkchannel"]

File = str
Folder = Dict[str, Union[File, Iterable['Folder']]]
text_ext_support = ['.py', '.txt', '.csv', '.ipynb']
binary_ext_support = ['.xlsx']


@fluent
class ModuleParser():
    """Module Parser"""
    def __init__(self, verbose: bool=True):
        self.modules: Folder = {}
        self.parsed_modules: str = None
        self.verbose: bool = verbose

    def parse_module(
            self,
            relative_module_path: str="."
        ) -> None:
        """Parse Module
        Function to parse module into a json file.
        :param path: path of the module
        """
        parent_path, module_path = os.path.split(relative_module_path)
        if self.verbose:
            print(f"\nParsing module: {relative_module_path}")

        self.parse_path(parent_path, self.modules, module_path, 0)

    def parse_path(self, parent_path, parent, path: str, layer: int=0) -> None:
        """General method to parse a given path"""
        full_path = os.path.join(parent_path, path)
        if path in parser_ignore:
            return

        if os.path.isfile(full_path):
            self.parse_file(parent_path, parent, path, layer)
        elif os.path.isdir(full_path):
            self.parse_folder(parent_path, parent, path, layer)
        else:
            raise FileExistsError(f"No file or directory: {full_path}")

    def parse_folder(self, parent_path, parent, folder_path: str, layer: int) -> None:
        """Parse folder to dictionary"""
        full_path = os.path.join(parent_path, folder_path)
        parent[full_path] = {}

        if self.verbose:
            print("   " * layer + f"{'|--'}  {folder_path}")

        for sub_path in glob.glob(os.path.join(full_path, "*")):
            sub_path = os.path.split(sub_path)[-1]
            self.parse_path(full_path, parent[full_path], sub_path, layer+1)

    def parse_file(self, parent_path, parent, file_name: str, layer: int) -> None:
        """Parse file into string"""
        full_path = os.path.join(parent_path, file_name)

        if self.verbose:
            print("   " * layer + f"{'|__'}  {file_name}")

        _, file_extension = os.path.splitext(file_name)

        if file_extension in text_ext_support:
            # Read text file
            with open(full_path, "r", encoding="utf-8") as file:
                parent[full_path] = encode_string(file.read())

        elif file_extension in binary_ext_support:
            # Read binary files
            with open(full_path, "rb") as file:
                parent[full_path] = encode_binary_string(file.read())
        else:
            raise NotImplementedError(
                f"File extension '{file_extension}' are currently not supported"
            )

    def module_to_json(self) -> None:
        """Convert modules dict to json"""
        self.parsed_modules = json.dumps(self.modules)

    def reconstruct_modules(self, base_path: str = "", force: bool = True) -> None:
        """Reconstruct the modules from the json string"""
        if os.path.exists(base_path) and not force:
            raise FileExistsError(f"Directory Exist {base_path}.")

        os.makedirs(base_path, exist_ok=True)
        loaded_modules: Dict[str, Folder] = json.loads(self.parsed_modules)

        for path, contains in loaded_modules.items():
            self.reconstruct_path(base_path, path, contains, force)

    def reconstruct_path(
            self,
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
                self.reconstruct_path(base_path, sub_path, sub_items, force)

        else:
            raise ValueError(f"Unknown file type {contains}")

    def generate_script(self):
        """Generate script to be eval on spark cluster"""
        self.module_to_json()

        real_path = os.path.dirname(os.path.realpath(__file__))
        script_path = os.path.join(real_path, "script.py")

        try:
            with open(script_path, "r", encoding="utf-8") as file:
                script = file.read()
        except:
            raise FileExistsError(f"Cannot read file: {script_path}")

        return script

    def show(self) -> None:
        """Show all parsed module"""
        print(json.dumps(self.modules,indent = 4))

    def __repr__(self) -> str:
        return ""

