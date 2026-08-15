import json
import os


class FileHandler:

    @staticmethod
    def write_json(file_path, data):
        directory = os.path.dirname(file_path)

        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=4,
                default=str
            )

    @staticmethod
    def read_json(file_path):
        if not os.path.exists(file_path):
            return None

        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
