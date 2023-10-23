from pydub import AudioSegment
import noisereduce as nr
import numpy as np
import silero
from pydub import AudioSegment
from IPython.display import Audio

#import librosa
def cleansimple():
    audio = AudioSegment.from_file("/home/wambugumuchemi/Projects/listen-write/audiobank/segment_1.mp3", format="mp3")
    clean_audio = audio.low_pass_filter(1200).high_pass_filter(200)
    #equalized_audio = clean_audio.equalize(band_range=(200, 4000))
    #preemphasized_audio = librosa.effects.preemphasis(clean_audio)

    # Export the processed audio to a new file
    clean_audio.export("cleansegment1.mp3", format="mp3")

def clean_audio_advanced(audio_path, output_path):
    # Load audio
    audio = AudioSegment.from_file(audio_path, format="mp3")

    # Convert to NumPy array
    audio_array = np.array(audio.get_array_of_samples())
    sr = audio.frame_rate
    # Perform noise reduction using noisereduce
    reduced_audio_array = nr.reduce_noise(audio_array, sr)

    # Create a new AudioSegment from the cleaned NumPy array
    cleaned_audio = AudioSegment(
        reduced_audio_array.tobytes(),
        frame_rate=audio.frame_rate,
        sample_width=audio.sample_width,
        channels=audio.channels
    )

    # Export the processed audio to a new file
    cleaned_audio.export(output_path, format="mp3")

def apply_silero_vad(input_path, output_path):
    # Load the audio
    audio = AudioSegment.from_file(input_path, format="mp3")

    # Convert audio to raw PCM
    pcm_data = audio.raw_data
    sample_width = audio.sample_width
    sample_rate = audio.frame_rate

    # Initialize Silero VAD

    vad = silero.Vad(device = 'cpu')
    
    #vad = SileroVAD(device='cpu')  # You can specify 'cuda' if you have a GPU

    # Apply VAD to the raw PCM data
    vad_result = vad.process_pcm(raw_data=pcm_data, sample_rate=sample_rate, sample_width=sample_width)

    # Convert the VAD result back to an AudioSegment
    vad_audio = AudioSegment(
        data=vad_result,
        sample_width=sample_width,
        frame_rate=sample_rate,
        channels=1  # Assuming mono audio
    )

    # Export the VAD-processed audio to a new file
    vad_audio.export(output_path, format="mp3")

# audio_path = "/home/wambugumuchemi/Projects/listen-write/only_speech.wav"
# output_path = "/home/wambugumuchemi/Projects/listen-write/cleaned_audio/clean1.mp3"

# clean_audio_advanced(audio_path, output_path)


#Lets first convert mp3 to wav

def mp3converter(audiopath):
    sound = AudioSegment.from_mp3(audiopath)
    sound.export( "en_example.wav", format="wav")
    return "en_example.wav"

    
#Audio("en_example.wav")
def silerovadit(audiopath):
    SAMPLING_RATE = 16000
    import torch
    torch.set_num_threads(1)

    from IPython.display import Audio
    from pprint import pprint
    # download example
    #torch.hub.download_url_to_file('https://models.silero.ai/vad_models/en.wav', 'en_example.wav')
    torch.hub.download_url_to_file(audiopath, 'en_example.mp3')
    #audio_file = "/home/wambugumuchemi/Projects/listen-write/audio.wav"
    #torch.hub.download_url_to_file('https://www.voiptroubleshooter.com/open_speech/american/OSR_us_000_0010_8k.wav', 'en_example.wav')

    audio = "en_example.mp3"
    mp3converter(audio)

    #Audio('en_example.wav')
    USE_ONNX = False # change this to True / False if you want to test onnx model
    if USE_ONNX:
        #%pip install -q onnxruntime
        print("Test feature, use this on ipynb")
    
    model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                model='silero_vad',
                                force_reload=True,
                                onnx=USE_ONNX)

    (get_speech_timestamps,
    save_audio,
    read_audio,
    VADIterator,
    collect_chunks) = utils

    wav = read_audio('en_example.wav', sampling_rate=SAMPLING_RATE)
    #wav = read_audio("/home/wambugumuchemi/Projects/listen-write/audio.wav", sampling_rate=SAMPLING_RATE)
    # get speech timestamps from full audio file
    speech_timestamps = get_speech_timestamps(wav, model, sampling_rate=SAMPLING_RATE)
    pprint(speech_timestamps)

    # merge all speech chunks to one audio
    save_audio('only_speech.wav',
            collect_chunks(speech_timestamps, wav), sampling_rate=SAMPLING_RATE) 
    #Audio('only_speech.wav')

