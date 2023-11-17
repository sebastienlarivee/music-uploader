import os
import json
import pyperclip


def copy_description_in_folder():
    """
    Find the 'metadata.json' file in the script's directory and copy the description to the clipboard.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    metadata_file = os.path.join(script_dir, "metadata.json")

    # Search for the metadata.json file in the script's directory
    if os.path.exists(metadata_file):
        try:
            with open(metadata_file, "r") as file:
                data = json.load(file)
                description = data.get("DESCRIPTION", "No description found")
                pyperclip.copy(description)
                print("Description copied to clipboard.")
        except Exception as e:
            print(f"Error occurred: {e}")
    else:
        print(f"'metadata.json' not found in the script's directory.")


if __name__ == "__main__":
    copy_description_in_folder()
