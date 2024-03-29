import os
import json
import pyperclip
from datetime import datetime


class YTDescription:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.metadata_path = os.path.join(folder_path, "metadata.json")
        self.metadata = {}

    def new_description(self):
        with open(self.metadata_path, "r") as file:
            self.metadata = json.load(file)
        description = self.generate_description()
        self.update_json(description)
        self.copy_to_clipboard(description)

    def generate_description(self):
        # Extracting the year from the 'DATE' key
        year = datetime.strptime(self.metadata["DATE"], "%Y-%m-%d").year

        description_header = (
            f"Perfect for background music, meditation, focus, study, relaxation, work, reading, gaming, or introspective moments. "
            f"Explore the boundless beauty and mystery of the cosmos with this Sci-Fi Ambient Space Soundtrack. 𝗜𝗳 𝘆𝗼𝘂'𝗿𝗲 𝗲𝗻𝗷𝗼𝘆𝗶𝗻𝗴 𝘁𝗵𝗲 𝗺𝗶𝘅 𝗽𝗹𝗲𝗮𝘀𝗲 𝗟𝗶𝗸𝗲 𝗮𝗻𝗱 𝗦𝘂𝗯𝘀𝗰𝗿𝗶𝗯𝗲!💕"
            f"\n\nAvailable on all platforms! Search: 'Ambient Archive {self.metadata['TITLE']}'"
            f"\n\n► Subscribe for more:\n\n / @ambientarchivemusic"
            f"\n\n► Spotify: https://open.spotify.com/artist/6TQSJ..."
            f"\n\n► Our Sci Fi Ambient Playlist:\n\n • Sci Fi Ambient Music 🌌"
            f"\n\n🎵 Music: {self.metadata['TITLE']} by Ambient Archive"
            f"\n🎨 Illustration: Stable Diffusion generated by Ambient Archive"
            f"\n\n🌌 About Ambient Archive:"
            f"\nAmbient Music for relaxation, work, study, introspection and almost any occasion. "
            f"We'll be releasing new music every week so make sure to Subscribe and enable notifications to join us on this cosmic journey!"
            f"\n\n{self.metadata['TITLE']} / Sci Fi Dark Ambient Space Music / Ambient Space Soundtrack {year}"
            f"\nThank you so much for listening and come again!"
            f"\n\n#AmbientMusic #SpaceMusic #SciFi #ExperimentalMusic #2023"
        )

        # Calculating the cumulative time for tracks
        cumulative_time = 0
        track_descriptions = []
        for track, length in zip(self.metadata["TRACKS"], self.metadata["LENGTH"]):
            # Rounding the cumulative time to the nearest second
            cumulative_time = round(cumulative_time)
            hours, remainder = divmod(cumulative_time, 3600)
            mins, secs = divmod(remainder, 60)
            track_descriptions.append(f"{hours:02}:{mins:02}:{secs:02} {track}")
            cumulative_time += length

        # Joining the formatted string and tracks
        description = description_header + "\n" + "\n".join(track_descriptions)
        return description

    def update_json(self, description):
        self.metadata["DESCRIPTION"] = description
        with open(self.metadata_path, "w") as file:
            json.dump(self.metadata, file, indent=4)

    def copy_to_clipboard(self, text):
        pyperclip.copy(text)
        print("Description copied to clipboard.")

    # Usage example:
    # processor = YTDescription('path_to_folder')
    # processor.new_description()
