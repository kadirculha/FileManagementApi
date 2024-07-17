import json


class Configurator:

    def __init__(self, path="config/config.json"):
        self.cfg = self.load_json(path)

    def get_base_path(self):
        return self.cfg["corridors_path"]

    @staticmethod
    def load_json(path, encoding="utf-8"):
        with open(path, encoding=encoding) as file:
            return json.load(file)

    @staticmethod
    def load_txt(path, encoding="utf-8"):
        with open(path, 'r', encoding=encoding) as f:
            return f.read().splitlines()
