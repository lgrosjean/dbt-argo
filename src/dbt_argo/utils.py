import yaml


def load_yaml(file_path):
    with open(file_path, "r", encoding="utf8") as file:
        file_dict = yaml.safe_load(file)
    return file_dict
