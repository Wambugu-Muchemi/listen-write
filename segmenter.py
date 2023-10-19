from pydub import AudioSegment
import os

def split_audio(input_file, output_folder, segment_duration=25):
    audio = AudioSegment.from_file(input_file)

    # Calculate the number of segments
    num_segments = len(audio) // (segment_duration * 1000)

    for i in range(num_segments):
        start_time = i * segment_duration * 1000
        end_time = (i + 1) * segment_duration * 1000

        # Extract the segment
        segment = audio[start_time:end_time]

        # Save the segment
        output_file = f"{output_folder}/segment_{i + 1}.mp3"
        segment.export(output_file, format="mp3")

if __name__ == "__main__":
    input_file = "/home/wambugumuchemi/Projects/listen-write/helloeeey.mp3"  # Change this to your audio file path
    output_folder = "./audiobank"  # Change this to your desired output folder

    # Create the output folder if it doesn't exist
    #os.makedirs(output_folder, exist_ok=True)

    split_audio(input_file, output_folder, segment_duration=25)
