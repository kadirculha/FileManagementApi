import os
import json
from config.config import Configurator
from config.input_params import RequestItem


class Director:
    def __init__(self):
        self.cfg = Configurator()
        self.base_path = self.cfg.get_base_path()  # "Corridors/"
        self.file_name = ""

    def get_path(self, item: RequestItem):
        if item.companyId:
            self.base_path = os.path.join(self.base_path, str(item.companyId))

        self.file_name = f"{item.corridor.id}.json"
        return self.base_path, self.file_name

    def check_file(self, base_path, file_name):
        file_path = os.path.join(base_path, file_name)
        return os.path.isfile(file_path)

    def write(self, base_path, file_name, content):
        os.makedirs(base_path, exist_ok=True)  # exist_ok: o yol zaten varsa oluşturmaz ve hata vermez

        file_path = os.path.join(base_path, file_name)
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(content, file, ensure_ascii=False, indent=4)

    def delete(self, base_path, file_name):
        file_path = os.path.join(base_path, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            return {"status": True, "message": f"File {file_path} has been deleted successfully."}
        else:
            return {"status":False,"message": f"File does not exist."}
        