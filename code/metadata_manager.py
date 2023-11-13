import json
import os


class MetadataManager:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.available_path = os.path.join(folder_path, "available.json")
        self.used_path = os.path.join(folder_path, "used.json")

    def _read_json(self, file_path):
        with open(file_path, "r") as file:
            return json.load(file)

    def _write_json(self, file_path, data):
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    def _move_terms(self, terms, from_category, to_category):
        available_data = self._read_json(self.available_path)
        used_data = self._read_json(self.used_path)

        for term in terms:
            available_data[from_category].remove(term)
            used_data[to_category].append(term)

        self._write_json(self.available_path, available_data)
        self._write_json(self.used_path, used_data)

    def _generate_roman_title_instances(self, title):
        roman_numerals = ["I", "II", "III", "IV"]
        return [f"{title} {numeral}" for numeral in roman_numerals]

    def create_metadata_folder(self):
        available_data = self._read_json(self.available_path)
        titles = available_data["TITLES"][:3]
        date = available_data["DATES"][0]

        new_folder_name = titles[0]
        albums_path = os.path.join(self.folder_path, "albums")
        new_folder_path = os.path.join(albums_path, new_folder_name)
        os.makedirs(new_folder_path)

        roman_title_instances = sum(
            [self._generate_roman_title_instances(title) for title in titles], []
        )

        metadata = {
            "TITLE": f"{titles[0]}",  # assuming you also want the first title to have a roman numeral
            "TRACKS": roman_title_instances,
            "DATE": date,
        }

        metadata_path = os.path.join(new_folder_path, "metadata.json")
        self._write_json(metadata_path, metadata)

        self._move_terms(titles, "TITLES", "TITLES")
        self._move_terms([date], "DATES", "DATES")

        return new_folder_path


# Usage example:
# manager = MetadataManager("/path/to/your/folder")
# new_folder_path = manager.create_metadata_folder()
