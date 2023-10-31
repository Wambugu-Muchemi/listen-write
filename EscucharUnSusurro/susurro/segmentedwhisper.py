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
from celery import Celery



#create a celery app instance
app = Celery('segmentedwhisper', broker='amqp://guest:guest@localhost:5672/')


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
@app.task
def maintask(source_url): 
    print("initiating main task...") 
    checkspeech = silerovadit(source_url)
    if checkspeech == 'only_speech.wav':
        segmentorun()
        #model = whisper.load_model("large-v2")
        # Load the model from the pickle file
        try:
            print("Loading model from Pickle")
            with open("whisper_model.pkl", "rb") as file:
                model = pickle.load(file)
            print("Model loaded")
        except:
            print("Model couldnt be processed from Pickle, loading from site.")
            model = whisper.load_model("large-v2")
            print("Model loaded but we shall pickle it for future use. Be patient.")
            model = whisper.load_model("large-v2")
            print("done pickling")
        audio_folder = "./audiobank"
        output_file = "./audiokon.txt"

        # Ensure the output file is empty
        open(output_file, 'w').close()

        # Loop through audio files in the folder and transcribe each segment
        # Get a list of all WAV files in the folder and sort them
        audio_files = [file_name for file_name in os.listdir(audio_folder) if file_name.endswith(".wav")]
        
        #audio_files.sort()

        # Natural sort the list
        audio_files = natsorted(audio_files)

        #for file_name in os.listdir(audio_folder):
        for file_name in audio_files:
            print("workin on",file_name)
            if file_name.endswith(".wav"):
                audio_path = os.path.join(audio_folder, file_name)
                transcribe_and_append(model, audio_path, output_file)
                os.remove(f"./audiobank/{file_name}")
        
        transcription = ""
        current_datetime = datetime.now()
        date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        # redefine TXT file
        txt_file_path = "./audiokon.txt"

        readtxtfile()
        txt_file_path = "./audiokonclean.txt"
        # Read the contents of the TXT file
        try:
            with open(txt_file_path, "r") as file:
                transcription = file.read()
            summary, issue_category = escribirAI(transcription)
            
            file.close()
            #store on db
            store_transcription_in_sqlite(source_url, transcription, date, summary, issue_category)
            return summary
        except Exception as e:
            return e

    else:
        print('No speech detected!')
        return 'No speech detected'
        


