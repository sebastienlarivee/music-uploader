from metadata_manager import MetadataManager
from album_organizer import AlbumOrganizer
from image_tools import ImageTools
from video_creator import VideoCreator
from yt_description import YTDescription
from ahk_script_generator import AHKScriptGenerator


def main():
    main_folder_path = "resources"
    artist_name = "Ambient Archive"

    # Create folder for the new album and its metadata
    manager = MetadataManager(main_folder_path, artist_name)
    album_folder_path = manager.create_metadata_folder()

    # Transfer .wav and .png files into album folder and rename accordingly
    organizer = AlbumOrganizer(main_folder_path, album_folder_path)
    rect_image_path = organizer.organize()
    organizer.add_length_metadata()

    # Create a square and thumbnail version of the .png
    square_and_thumbnail = ImageTools(rect_image_path, square_size=1080, max_mb=2)
    square_and_thumbnail.make_square_and_thumbnail()

    # Render video for YouTube
    video_creator = VideoCreator(album_folder_path)
    video_creator.create_video()

    # Generate YouTube description + chapters -> automatically copy to clipboard
    description = YTDescription(album_folder_path)
    description.new_description()

    # Generate AHK script for fast DistrKid uploads
    ahk_script_generator = AHKScriptGenerator(album_folder_path)
    ahk_script_generator.run()


if __name__ == "__main__":
    main()
