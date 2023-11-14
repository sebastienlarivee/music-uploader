import os
import shutil
import json
import wave


class AlbumOrganizer:
    def __init__(self, main_folder, album_folder):
        self.main_folder = main_folder
        self.album_folder = album_folder

    def organize(self):
        wav_folder = os.path.join(self.main_folder, "wavs")
        png_folder = os.path.join(self.main_folder, "pngs")
        metadata_file = os.path.join(self.album_folder, "metadata.json")

        # Check if the wavs folder, pngs folder and metadata file exist
        if (
            not os.path.exists(wav_folder)
            or not os.path.exists(png_folder)
            or not os.path.exists(metadata_file)
        ):
            raise FileNotFoundError(
                "Wavs folder, pngs folder, or metadata file not found."
            )

        # Get the first 12 .wav files from the wavs folder
        wav_files = [f for f in os.listdir(wav_folder) if f.endswith(".wav")][:12]

        # Check if there are at least 12 wav files
        if len(wav_files) < 12:
            raise FileNotFoundError("Not enough wav files in the wavs folder.")

        # Load metadata file
        with open(metadata_file, "r") as file:
            metadata = json.load(file)
            tracks = metadata.get("TRACKS", [])
            title = metadata.get("TITLE")

        # Check if TRACKS has 12 entries
        if len(tracks) < 12:
            raise ValueError("TRACKS in metadata file does not have 12 entries.")

        # Check if TITLE is available
        if not title:
            raise ValueError("TITLE not found in metadata file.")

        # Move and rename wav files
        for index, (wav_file, track) in enumerate(zip(wav_files, tracks), start=1):
            src = os.path.join(wav_folder, wav_file)
            dst = os.path.join(self.album_folder, f"{index} {track}.wav")
            shutil.move(src, dst)

        # Move and rename the first png file
        png_files = [f for f in os.listdir(png_folder) if f.endswith(".png")]
        if png_files:
            src = os.path.join(png_folder, png_files[0])
            dst = os.path.join(self.album_folder, f"{title}.png")
            shutil.move(src, dst)
            return dst  # Return the path to the moved and renamed png file
        else:
            raise FileNotFoundError("No png files found in the pngs folder.")

    def add_length_metadata(self):
        metadata_file = os.path.join(self.album_folder, "metadata.json")

        # Check if metadata file exists
        if not os.path.exists(metadata_file):
            raise FileNotFoundError("Metadata file not found.")

        # Load existing metadata
        with open(metadata_file, "r") as file:
            metadata = json.load(file)

        # Ensure TRACKS exists and has 12 entries
        tracks = metadata.get("TRACKS", [])
        if len(tracks) < 12:
            raise ValueError("TRACKS in metadata file does not have 12 entries.")

        # Get the length of each track
        lengths = []
        for index, track in enumerate(tracks, start=1):
            track_file = os.path.join(self.album_folder, f"{index} {track}.wav")
            if not os.path.exists(track_file):
                raise FileNotFoundError(f"Track file not found: {track_file}")

            with wave.open(track_file, "rb") as wav_file:
                frames = wav_file.getnframes()
                rate = wav_file.getframerate()
                length_seconds = frames / float(rate)
                lengths.append(round(length_seconds, 2))

        # Update metadata with LENGTH
        metadata["LENGTH"] = lengths

        # Write updated metadata back to file
        with open(metadata_file, "w") as file:
            json.dump(metadata, file, indent=4)


# Usage:
# main_folder_path = "/path/to/main/folder"
# album_folder_path = "/path/to/album/folder"

# organizer = AlbumOrganizer(main_folder_path, album_folder_path)
# organizer.organize()
# organizer.add_length_metadata()
