from typing import List


class Validator:
    def is_valid_data_input(self, expected_headers: List[str], content_data: List[dict], content_data_keys: List[str]) -> bool:
        if not all(isinstance(row, dict) for row in content_data):
            return False
        return content_data_keys == self.__process_headers(expected_headers)

    def has_valid_headers(self, file_path: str, expected_headers: List[str]) -> bool:
        with open(file_path, 'r') as file:
            headers_from_file = file.readline().strip().split(',')
            return headers_from_file == self.__process_headers(expected_headers)

    def __process_headers(self, headers: List[str]) -> List[str]:
        return ','.join(headers).strip().split(',')
