from pydub import AudioSegment
import os

def split_audio(input_file, output_folder, segment_duration=25):
    """
    Split the input audio file into segments of a specified duration and save them in WAV format.

    Args:
    - input_file: The path to the input audio file.
    - output_folder: The path to the folder where the segments will be saved.
    - segment_duration: The duration of each segment in seconds.
    """
    print("Segmenting...")
    audio = AudioSegment.from_file(input_file)

    # Calculate the number of segments
    num_segments = len(audio) // (segment_duration * 1000)
    print(f"{num_segments} segments found.")

    for i in range(num_segments):
        start_time = i * segment_duration * 1000
        end_time = (i + 1) * segment_duration * 1000

        # Extract the segment
        segment = audio[start_time:end_time]

        # Save the segment in WAV format
        output_file = f"{output_folder}/segment_{i + 1}.wav"
        segment.export(output_file, format="wav")
        print(f"{output_file} processed.")

    # Handle the last segment
    last_segment = audio[num_segments * segment_duration * 1000:]
    if len(last_segment) > 0:
        output_file = f"{output_folder}/segment_{num_segments + 1}.wav"
        last_segment.export(output_file, format="wav")

def segmentorun():
    input_file = "./only_speech.wav"  # Change this to your audio file path
    output_folder = "./audiobank"  # Change this to your desired output folder

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    split_audio(input_file, output_folder, segment_duration=25)

if __name__ == "__main__":
    segmentorun()
