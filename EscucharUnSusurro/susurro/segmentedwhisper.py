import os
import whisper
from segmenter import *
from cleanaudio import *
from storage import *
from summarizeAI import *
from datetime import date, datetime
from natsort import natsorted
import pickle
from picklethemodel import picklenow
from textcleaner import *

def transcribe_and_append(model, audio_path, output_file):
    """
    Transcribe the audio at the given path using the provided model
    and append the result to the specified output file.

    Args:
    - model: The whisper ASR model.
    - audio_path: The path to the audio file.
    - output_file: The file to append the transcription result to.
    """
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
    # Get user input for transcription URL and customer contact
    source_url = input("Enter your transcription URL: ")
    contact = input("Enter customer contact: ")

    # Check if speech is present in the provided URL
    checkspeech = silerovadit(source_url)
    if checkspeech == 'only_speech.wav':
        # Segment the audio
        segmentorun()

        # Load the model from the pickle file, or from the site if pickle fails
        try:
            print("Loading model from Pickle")
            with open("whisper_model.pkl", "rb") as file:
                model = pickle.load(file)
            print("Model loaded")
        except:
            print("Model couldn't be processed from Pickle, loading from site.")
            model = whisper.load_model("large")
            print("Model loaded but we shall pickle it for future use. Be patient.") 
            picklenow()
            print("Done pickling")

        # Set the audio folder and output file paths
        audio_folder = "./audiobank"
        output_file = "./audiokon.txt"

        # Ensure the output file is empty
        open(output_file, 'w').close()

        # Get a list of all WAV files in the folder and sort them
        audio_files = [file_name for file_name in os.listdir(audio_folder) if file_name.endswith(".wav")]

        # Natural sort the list
        audio_files = natsorted(audio_files)

        # Process each audio file, transcribe, and remove the original file
        for file_name in audio_files:
            print("Working on", file_name)
            if file_name.endswith(".wav"):
                audio_path = os.path.join(audio_folder, file_name)
                transcribe_and_append(model, audio_path, output_file)
                os.remove(f"./audiobank/{file_name}")

        # Process the transcriptions and store them in the database
        transcription = ""
        current_datetime = datetime.now()
        date_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        
        # Read the contents of the cleaned TXT file
        input_file_path = './audiokon.txt'
        output_file_path = './audiokonclean.txt'
        read_and_clean_text(input_file_path,output_file_path)
        txt_file_path = "./audiokonclean.txt"
        with open(txt_file_path, "r") as file:
            transcription = file.read()
        summary, issue_category = escribir_AI(transcription)
        print(summary)
        
        # Store the transcription in the SQLite database
        store_transcription_in_sqlite(source_url, transcription, date_str, summary, issue_category, contact)
    else:
        print('No speech detected!')
        pass

if __name__ == "__main__":
    main()
