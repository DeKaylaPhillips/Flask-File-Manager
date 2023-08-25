import os
import csv
from typing import *


class Validator:
    pass


class Formatter:
    pass


class FileHandler:
    BASE_DIR = 'files'

    def __init__(self, Validator: Type[Validator], Formatter: Type[Formatter]) -> None:
        self.validate = Validator()
        self.format = Formatter()

    def create_csv_file(self, filename: str, headers: List[str]) -> None:
        if not headers:
            raise ValueError("Headers are required for CSV files.")
        elif not os.path.exists(FileHandler.BASE_DIR):
            os.makedirs(FileHandler.BASE_DIR, exist_ok=True)
        file_path = os.path.join(FileHandler.BASE_DIR, filename)
        with open(file_path, 'w') as file:
            formatted_headers = self.format.get_csv_formatted_headers(headers)
            file.write(formatted_headers)
        return True

    def read(self, filename: str):
        file_path = os.path.join(FileHandler.BASE_DIR, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file '{filename}' does not exist.")
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            content = list(row for row in reader)
        return content

    def update(self, filename: str, content_data: List[dict], expected_headers: List[str]) -> bool:
        file_path = os.path.join(FileHandler.BASE_DIR, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file '{filename}' does not exist.")
        elif not self.validate.has_valid_headers(file_path, expected_headers):
            raise ValueError("No valid headers found in CSV files.")
        content_data_keys = [
            key for header in content_data for key in header.keys()]
        if not self.validate.is_valid_data_input(expected_headers, content_data, content_data_keys):
            raise ValueError("Incorrect data structure provided.")
        with open(file_path, 'a') as file:
            formatted_data = self.format.get_csv_formatted_data(content_data)
            file.writelines(formatted_data)
        return True

    def delete(self, filename: str):
        file_path = os.path.join(FileHandler.BASE_DIR, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file '{filename}' does not exist.")
        os.remove(file_path)
