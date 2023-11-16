from moviepy.editor import *
import glob
import os


class VideoCreator:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.image_path = self.find_image()
        self.audio_paths = self.find_and_sort_audio_files()
        self.output_path = self.determine_output_path()

    def find_image(self):
        # Select the only image file without an underscore in its name
        for file_name in os.listdir(self.folder_path):
            if file_name.endswith(".png") and "_" not in file_name:
                return os.path.join(self.folder_path, file_name)
        raise FileNotFoundError(f"No suitable .png file found in {self.folder_path}")

    @staticmethod
    def sorting_key(file_path):
        # Extract the file name from the file path
        file_name = os.path.basename(file_path)
        # Split the file name on spaces and take the first part, which should be the number
        number_str = file_name.split(" ")[0]
        # Convert the number string to an integer
        return int(number_str)

    def find_and_sort_audio_files(self):
        audio_paths = sorted(
            glob.glob(os.path.join(self.folder_path, "*.wav")), key=self.sorting_key
        )
        if not audio_paths:
            raise FileNotFoundError(f"No .wav files found in {self.folder_path}")
        return audio_paths

    def determine_output_path(self):
        return os.path.join(
            self.folder_path, f"{os.path.basename(self.folder_path)}.mp4"
        )

    def create_video(self):
        # Load image and set duration
        image_clip = ImageClip(self.image_path)

        # Load and concatenate audio clips
        audio_clips = [AudioFileClip(audio_path) for audio_path in self.audio_paths]
        concatenated_audio = concatenate_audioclips(audio_clips)

        # Set the duration of the image clip to match the audio duration
        image_clip = image_clip.set_duration(concatenated_audio.duration)

        # Set the concatenated audio to the image clip
        video_clip = image_clip.set_audio(concatenated_audio)

        # Write the result to a file, specifying fps and audio bitrate
        print("Rendering video...")
        video_clip.write_videofile(
            self.output_path,
            fps=1,
            codec="libx264",
            audio_codec="aac",
            audio_bitrate="384k",  # Higher audio bitrate
            bitrate="500k",
            threads=8,  # Utilize multiple threads for faster rendering
        )


# Usage:
# video_creator = VideoCreator(folder/path)
# video_creator.create_video()
