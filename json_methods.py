import json


def read_json(file):
    with open(file, 'r') as file_handle:
        return json.load(file_handle)


def write_json(file, dump_list):
    with open(file, 'w') as file_handle:
        json.dump(dump_list, file_handle, indent=4)
