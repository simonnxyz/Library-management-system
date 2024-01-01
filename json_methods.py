import json


def read_json(file):
    """
    Reads and parses JSON data from a file.
    """
    with open(file) as file_handle:
        return json.load(file_handle)


def write_json(file, dump_list):
    """
    Writes a list or dictionary as JSON data to a file.
    """
    with open(file, 'w') as file_handle:
        json.dump(dump_list, file_handle, indent=4, default=str)
