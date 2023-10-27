from pydub import AudioSegment
import os

def split_audio(input_file, output_folder, segment_duration=25):
    print("segmenting ...")
    audio = AudioSegment.from_file(input_file)

    # Calculate the number of segments
    num_segments = len(audio) // (segment_duration * 1000)
    print(num_segments, " segments found.")

    for i in range(num_segments):
        start_time = i * segment_duration * 1000
        end_time = (i + 1) * segment_duration * 1000

        # Extract the segment
        segment = audio[start_time:end_time]

        # # Save the segment in mp3
        # output_file = f"{output_folder}/segment_{i + 1}.mp3"
        # segment.export(output_file, format="mp3")

        # Save the segment in wav
        output_file = f"{output_folder}/segment_{i + 1}.wav"
        segment.export(output_file, format="wav")
        print(output_file, ' processed.')
    # Handle the last segment
    last_segment = audio[num_segments * segment_duration * 1000:]
    if len(last_segment) > 0:
        output_file = f"{output_folder}/segment_{num_segments + 1}.wav"
        last_segment.export(output_file, format="wav")

def segmentorun():
    input_file = "/home/wambugumuchemi/Projects/listen-write/only_speech.wav"  # Change this to your audio file path
    output_folder = "./audiobank"  # Change this to your desired output folder

    # Create the output folder if it doesn't exist
    #os.makedirs(output_folder, exist_ok=True)

    split_audio(input_file, output_folder, segment_duration=25)

if __name__ == "__main__":
    # input_file = "/home/wambugumuchemi/Projects/listen-write/only_speech.wav"  # Change this to your audio file path
    # output_folder = "./audiobank"  # Change this to your desired output folder

    # # Create the output folder if it doesn't exist
    # #os.makedirs(output_folder, exist_ok=True)

    # split_audio(input_file, output_folder, segment_duration=25)
    segmentorun()
