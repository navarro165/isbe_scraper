import os
import json


def join_files():
    json_folder_path = "/Users/cnavarro/Downloads/Attachments-jsons"
    paths = [os.path.join(json_folder_path, _) for _ in os.listdir(json_folder_path)]

    joined = {}
    for _path in paths:
        with open(_path, 'r') as myfile:
            data = myfile.read()

        joined.update(json.loads(data))

    with open('sample_joined_records.json', 'w') as json_file:
        json.dump(joined, json_file)


def collect_scraped_values():
    with open("sample_scraped_values.txt", 'r') as file:
        contents = file.read().replace('\n', '').rstrip(",")
        contents = json.loads(f"[{contents}]")

        parsed_contents = {}
        for line_dict in contents:
            parsed_contents.update(line_dict)

    return parsed_contents


def export_collected():
    data = collect_scraped_values()
    with open('sample_scraped_values.json', 'w') as outfile:
        json.dump(data, outfile)


if __name__ == '__main__':

    export_collected()
