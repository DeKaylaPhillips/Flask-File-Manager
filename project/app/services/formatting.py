class Formatter:
    def get_csv_formatted_data(self, data_list):
        data = [value for key in data_list for value in key.values()]
        return self.__csv_formatter(data)

    def get_csv_formatted_headers(self, headers_list):
        return self.__csv_formatter(headers_list)

    def __csv_formatter(self, data):
        return ','.join(data) + '\n'
