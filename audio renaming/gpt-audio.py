import os
from moviepy.editor import VideoFileClip
import pandas as pd

# Read the spreadsheet containing DATE, MIN, SEC, and LEN
#spreadsheet_path = 'path/to/your/spreadsheet.xlsx'  # Update with your spreadsheet path
spreadsheet_path = r'C:\Users\malat\Downloads\Takeout\Recorder\dates-and-lengths.ods'
df = pd.read_excel(spreadsheet_path)
df.columns = ['col1', 'col2', 'col3', 'date', 'col5', 'min', 'sec']

# Path to the folder containing .mp4 files
# audio_folder_path = 'path/to/your/audio/folder/'  # Update with your audio files folder path
audio_folder_path = r'C:\Users\malat\Downloads\Takeout\Recorder'

print(df.head())


# Iterate through each row in the spreadsheet
for index, row in df.iterrows():
    date = row['date']
    minutes = row['min']
    seconds = row['sec']
    length = minutes * 60 + seconds  # Convert minutes to seconds and add to seconds

    file_name = f"{date}-{row['NAME']}"

    # Check if file exists in the specified folder
    file_path = os.path.join(audio_folder_path, f"{file_name}.mp4")

    if os.path.isfile(file_path):
        # Get the duration of the audio file
        clip = VideoFileClip(file_path)
        duration = round(clip.duration)  # Round to the nearest second
        clip.close()

        # Check if the duration matches the length in the spreadsheet
        if duration == length:
            # Rename the file with the new format
            new_file_name = f"{date}-{row['NAME']}"
            new_file_path = os.path.join(audio_folder_path, f"{new_file_name}.mp4")
            os.rename(file_path, new_file_path)
        else:
            # Add special label for unmatched recordings
            new_file_name = f"UNCAT-{row['NAME']}"
            new_file_path = os.path.join(audio_folder_path, f"{new_file_name}.mp4")
            os.rename(file_path, new_file_path)
    else:
        # Handle the case where the file doesn't exist
        print(f"File not found: {file_path}")

# Manual check for recordings with exactly the same timestamp
# Add the "UNCAT" label to those entries in the spreadsheet
# Save the updated spreadsheet
df.to_excel(spreadsheet_path, index=False)

