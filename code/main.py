from image_tools import *
from metadata_manager import *
from album_organizer import *
from image_tools import *
from video_creator import *
from yt_description import *

# Specify folder that contains /wavs, /pngs, available.json, and used.json
main_folder_path = r"resources"

# Create folder for the new album and its metadata
manager = MetadataManager(main_folder_path)
album_folder_path = manager.create_metadata_folder()

# Transfer .wav and .png files into album folder and rename accordingly
organizer = AlbumOrganizer(main_folder_path, album_folder_path)
rect_image_path = organizer.organize()
organizer.add_length_metadata()

# Create a square and thumbnail version of the .png
cropper = ImageCropper(rect_image_path, 1080)
cropper.save_cropped_image_same_location()
resizer = ImageResizer(rect_image_path)
resizer.save_resized_image_same_location()

# Create video for Youtube
video_creator = VideoCreator(album_folder_path)
video_creator.create_video()

# Generate Youtube description + chapters -> automatically copy to clipboard
description = YTDescription(album_folder_path)
description.new_description()


# Upload to DistroKid with selenium