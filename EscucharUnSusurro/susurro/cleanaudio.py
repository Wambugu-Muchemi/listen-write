from sys import exception
from pydub import AudioSegment
import noisereduce as nr
import numpy as np
import silero
import librosa
import soundfile as sf

def cleansimple(daudio):
    """
    Apply a low-pass filter (200 Hz) and a high-pass filter (1200 Hz) to the audio.
    
    Args:
    - daudio: The path to the audio file.
    """
    print("Passing pre-Sileroed audio through audiowash")
    audio = AudioSegment.from_file(daudio, format="mp3")
    clean_audio = audio.low_pass_filter(1200).high_pass_filter(200)
    clean_audio.export(daudio, format="mp3")
    print("Audiowash complete")

def cleansimplewithspectralgating(daudio):
    """
    Apply spectral gating to the audio using librosa.effects.trim.
    
    Args:
    - daudio: The path to the audio file.
    """
    print("Running with spectral gating")
    audio_signal, sample_rate = librosa.load(daudio, sr=None, mono=True)
    trimmed_audio, _ = librosa.effects.trim(audio_signal, top_db=20, frame_length=512, hop_length=64)
    sf.write(daudio, trimmed_audio, sample_rate)

def clean_audio_advanced(audio_path, output_path):
    """
    Perform advanced audio cleaning using noisereduce.

    Args:
    - audio_path: The path to the input audio file.
    - output_path: The path to save the cleaned audio.
    """
    audio = AudioSegment.from_file(audio_path, format="mp3")
    audio_array = np.array(audio.get_array_of_samples())
    sr = audio.frame_rate
    reduced_audio_array = nr.reduce_noise(audio_array, sr)
    cleaned_audio = AudioSegment(
        reduced_audio_array.tobytes(),
        frame_rate=audio.frame_rate,
        sample_width=audio.sample_width,
        channels=audio.channels
    )
    cleaned_audio.export(output_path, format="mp3")

def apply_silero_vad(input_path, output_path):
    """
    Apply Silero VAD (Voice Activity Detection) to the audio.

    Args:
    - input_path: The path to the input audio file.
    - output_path: The path to save the VAD-processed audio.
    """
    audio = AudioSegment.from_file(input_path, format="mp3")
    pcm_data = audio.raw_data
    sample_width = audio.sample_width
    sample_rate = audio.frame_rate

    try:
        vad = silero.Vad(device='cpu')
        vad_result = vad.process_pcm(raw_data=pcm_data, sample_rate=sample_rate, sample_width=sample_width)
        vad_audio = AudioSegment(
            data=vad_result,
            sample_width=sample_width,
            frame_rate=sample_rate,
            channels=1
        )
        vad_audio.export(output_path, format="mp3")
    except Exception as e:
        print(f"Error processing audio with Silero VAD: {e}")

def mp3converter(audiopath):
    """
    Convert MP3 audio to WAV format.

    Args:
    - audiopath: The path to the MP3 audio file.

    Returns:
    - The path to the converted WAV file.
    """
    print(audiopath)
    sound = AudioSegment.from_mp3(audiopath)
    wav_path = "en_example.wav"
    sound.export(wav_path, format="wav")
    return wav_path

def silerovadit(audiopath):
    """
    Apply Silero VAD and return the path to the VAD-processed audio.

    Args:
    - audiopath: The path to the input audio file.

    Returns:
    - The path to the VAD-processed audio file.
    """
    SAMPLING_RATE = 16000
    import torch
    torch.set_num_threads(1)

    from IPython.display import Audio
    from pprint import pprint
    try:
        torch.hub.download_url_to_file(audiopath, 'en_example.mp3')
    except Exception as e:
        print(f"Download URL issue: {e}")
        return 'no silero'
    
    audio = mp3converter("en_example.mp3")

    USE_ONNX = False
    if USE_ONNX:
        print("Test feature, use this on ipynb")

    model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad', force_reload=True, onnx=USE_ONNX)
    (get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks) = utils

    wav = read_audio(audio, sampling_rate=SAMPLING_RATE)
    
    try:
        speech_timestamps = get_speech_timestamps(wav, model, sampling_rate=SAMPLING_RATE)
        save_audio('only_speech.wav', collect_chunks(speech_timestamps, wav), sampling_rate=SAMPLING_RATE) 
        return 'only_speech.wav'
    except Exception as e:
        print(f"Error processing audio with Silero VAD: {e}")
        import os
        os.rename('en_example.wav', 'only_speech.wav')
        return 'no silero'
