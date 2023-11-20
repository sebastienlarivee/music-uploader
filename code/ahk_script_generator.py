import os
import json
from datetime import datetime


class AHKScriptGenerator:
    def __init__(self, folder_path):
        self.folder_path = os.path.abspath(folder_path)
        self.metadata_file = "metadata.json"
        self.title = ""
        self.tracks = []
        self.date = ""
        self.artist_name = ""

    def read_metadata(self):
        """Reads the metadata.json file and extracts the TITLE, TRACKS, and DATE data."""
        try:
            with open(os.path.join(self.folder_path, self.metadata_file), "r") as file:
                data = json.load(file)
                self.artist_name = data.get("ARTIST", "")
                self.title = data.get("TITLE", "")
                self.tracks = data.get("TRACKS", [])

                date_str = data.get("DATE", "")
                if date_str:
                    parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
                    self.date = [
                        parsed_date.strftime("%Y"),
                        parsed_date.strftime("%B"),
                        parsed_date.strftime("%d"),
                    ]
                else:
                    self.date = []
        except FileNotFoundError:
            print(f"metadata.json not found in {self.folder_path}")
        except json.JSONDecodeError:
            print("Error decoding JSON from metadata.json")

    def generate_ahk_script(self):
        """Generates the AHK script based on the metadata."""
        if not self.title or not self.tracks:
            print("Title or tracks not found in metadata.json")
            return

        ahk_script_content = "^j::\n\n"
        ahk_script_content += "    SetKeyDelay, 200\n\n"
        ahk_script_content += "    Send, {Tab}\n"
        ahk_script_content += f"    Send, {len(self.tracks)}\n"
        ahk_script_content += "    Sleep, 2000\n"
        ahk_script_content += "    Send, {Tab 2}\n"
        ahk_script_content += f"    SendInput, {self.artist_name}\n"  # Artist name
        ahk_script_content += "    Sleep, 2000\n"
        ahk_script_content += "    Send, {Tab 3}\n"
        ahk_script_content += f"    Send, {self.date[1]}\n"  # Month
        ahk_script_content += "    Send, {Tab}\n"
        ahk_script_content += f"    Send, {self.date[2]}\n"  # Day
        ahk_script_content += "    Send, {Tab}\n"
        ahk_script_content += f"    Send, {self.date[0]}\n"  # Year
        ahk_script_content += "    Send, {Tab 10}\n"
        ahk_script_content += "    Send, electronic\n"  # Genre
        ahk_script_content += "    Sleep, 1000\n"
        ahk_script_content += "    Send, {Tab}\n"
        ahk_script_content += "    Send, chill out\n"  # Sub-genre
        ahk_script_content += "    Send, {Tab 2}\n"
        ahk_script_content += "    Send, {Enter}\n"
        ahk_script_content += "    Sleep, 2000\n"
        ahk_script_content += (
            f"    SendInput, {self.folder_path}\{self.title}_square.png\n"
        )
        ahk_script_content += "    Send, {Enter}\n"
        ahk_script_content += "    Sleep, 2000\n"
        ahk_script_content += "    Send, {Tab}\n"
        ahk_script_content += f"    SendInput, {self.title}\n"
        ahk_script_content += "    Send, {Tab}\n\n"

        for track in self.tracks:
            ahk_script_content += f"    SendInput, {track}\n"
            ahk_script_content += "    Send, {Tab 3}\n"
            ahk_script_content += "    Send, {Enter}\n"
            ahk_script_content += "    Sleep, 2000\n"
            ahk_script_content += f"    SendInput, {self.folder_path}\{self.tracks.index(track) + 1} {track}.wav\n"
            ahk_script_content += "    Send, {Enter}\n"
            ahk_script_content += "    Sleep, 2000\n"
            ahk_script_content += "    Send, {Tab 11}\n"
            ahk_script_content += "    Send, {Down}\n"
            ahk_script_content += "    Send, {Tab 3}\n\n"

        ahk_script_path = os.path.join(self.folder_path, f"{self.title}.ahk")
        with open(ahk_script_path, "w") as file:
            file.write(ahk_script_content)
        print(f"AHK script saved as {ahk_script_path}")

    def run(self):
        """Executes the entire process."""
        self.read_metadata()
        self.generate_ahk_script()

    # Usage
    # ahk_script_generator = AHKScriptGenerator(folder_path)
    # ahk_script_generator.run()
