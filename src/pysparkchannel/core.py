"""Module Parser

Parse a module into a text files.
"""
import glob
import json
import os
from pysparkchannel.utils import fluent

@fluent
class ModuleParser():
    """Module Placer"""
    def __init__(self):
        self.modules = {}
        self.parsed_modules: str = None

    def parse_module(self, module_path: str=".") -> None:
        """Parse Module
        Function to parse module into a json file.
        :param path: path of the module
        """
        self.parse_path(".", self.modules, module_path, 0)

    def parse_path(self, parent_path, parent, path: str, layer: int=0) -> None:
        """General method to parse a given path"""
        full_path = os.path.join(parent_path, path)
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
        print(" |_" * layer + f"parsing {full_path}")
        for sub_path in glob.glob(os.path.join(full_path, "*")):
            sub_path = os.path.split(sub_path)[-1]
            self.parse_path(full_path, parent[full_path], sub_path, layer+1)

    def parse_file(self, parent_path, parent, file_name: str, layer: int) -> None:
        """Parse file into string"""
        full_path = os.path.join(parent_path, file_name)
        print(" |_" * layer + f"parsing {file_name}")
        with open(full_path, "r", encoding="utf-8") as file:
            parent[full_path] = file.read()

    def module_to_json(self) -> None:
        """Convert modules dict to json"""
        self.parsed_modules = json.dumps(self.modules)

    def reconstruct_modules(self) -> None:
        pass

    def show(self) -> None:
        """Show all parsed module"""
        print(self.modules)

    def __repr__(self) -> str:
        return ""

if __name__ == "__main__":

    parser = ModuleParser()
    parser \
        .parse_module("ModuleA") \
        .parse_module("ModuleB") \
        .reconstruct_modules()
