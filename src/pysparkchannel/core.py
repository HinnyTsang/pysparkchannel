"""Module Parser

Parse a module into a text files.
"""
from utils import fluent
from collections import defaultdict
import glob


@fluent
class ModuleParser():
    """Module Placer"""
    def __init__(self):
        self.modules = []

    def parse_module(self, module_path: str=".") -> None:
        """Parse Module
        Function to parse module into a json file.
        :param path: path of the module
        """
        _ = module_path

    def parse_path(self, path: str) -> None:
        """General method to parse a given path"""
        pass

    def parse_folder(self, folder_path: str) -> None:
        pass
    
    def parse_file(self, parent, file_name: str) -> None:
        """Parse file into string"""
        with open(file_name, "r", encoding="utf-8") as file:
            parent[file_name] = file.read()
    
    def reconstruct_modules(self) -> None:
        pass

if __name__ == "__main__":

    parser = ModuleParser()
    parser \
        .parse_module("ModuleA") \
        .parse_module("ModuleB") \
        .reconstruct_modules()
