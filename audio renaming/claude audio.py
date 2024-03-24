import os
from moviepy.editor import AudioFileClip
import pandas as pd

# Set the paths
audio_folder_path = r'C:\Users\malat\Downloads\Takeout\Recorder'
spreadsheet_path = r'C:\Users\malat\Downloads\Takeout\Recorder\dates-and-lengths.ods'

# Load the spreadsheet
df = pd.read_excel(spreadsheet_path, engine='odf')

# Get the column names
column_names = df.columns

# Find the indices of the date, min, and sec columns
date_col = column_names[column_names.str.contains('DATE', case=False)].values[0]
min_col = column_names[column_names.str.contains('MIN', case=False)].values[0]
sec_col = column_names[column_names.str.contains('SEC', case=False)].values[0]

# Function to get the duration of an audio file in seconds
def get_audio_duration(file_path):
    clip = AudioFileClip(file_path)
    duration = clip.duration
    clip.close()
    return int(duration)

# Iterate through the files in the audio folder
for filename in os.listdir(audio_folder_path):
    if filename.endswith('.m4a'):
        file_path = os.path.join(audio_folder_path, filename)
        duration = get_audio_duration(file_path)
        duration_seconds = duration

        # Find the corresponding date from the spreadsheet
        for idx, row in df.iterrows():
            minutes = row[min_col]
            seconds = row[sec_col]
            audio_duration_seconds = int(minutes) * 60 + int(seconds)
            if audio_duration_seconds == duration_seconds:
                date = row[date_col].date()
                new_filename = f"{date}_{filename}"
                new_file_path = os.path.join(audio_folder_path, new_filename)
                os.rename(file_path, new_file_path)
                print(f"Renamed '{filename}' to '{new_filename}'")
                break