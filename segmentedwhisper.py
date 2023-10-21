import os
import whisper

def transcribe_and_append(model, audio_path, output_file):
    with open(output_file, 'a') as f:
        # load audio and pad/trim it to fit 30 seconds
        audio = whisper.load_audio(audio_path)
        audio = whisper.pad_or_trim(audio)

        # make log-Mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(audio).to(model.device)

        # detect the spoken language
        _, probs = model.detect_language(mel)
        detected_language = max(probs, key=probs.get)

        # decode the audio
        options = whisper.DecodingOptions(fp16=False)
        result = whisper.decode(model, mel, options)

        # print the recognized text
        transcription = result.text
        f.write(f"File: {os.path.basename(audio_path)} (Language: {detected_language}):\n")
        f.write(transcription + '\n\n')

def main():
    model = whisper.load_model("large")
    audio_folder = "/home/wambugumuchemi/Projects/listen-write/audiobank"
    output_file = "/home/wambugumuchemi/Projects/listen-write/audiokon3.txt"

    # Ensure the output file is empty
    open(output_file, 'w').close()

    # Loop through audio files in the folder and transcribe each segment
    # Get a list of all WAV files in the folder and sort them
    audio_files = [file_name for file_name in os.listdir(audio_folder) if file_name.endswith(".wav")]
    audio_files.sort()
    #for file_name in os.listdir(audio_folder):
    for file_name in audio_files:
        print("workin on",file_name)
        if file_name.endswith(".wav"):
            audio_path = os.path.join(audio_folder, file_name)
            transcribe_and_append(model, audio_path, output_file)

if __name__ == "__main__":
    main()
