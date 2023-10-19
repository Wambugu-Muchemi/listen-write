from pydub import AudioSegment
import noisereduce as nr
import numpy as np
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

audio_path = "/home/wambugumuchemi/Projects/listen-write/audiobank/segment_1.mp3"
output_path = "/home/wambugumuchemi/Projects/listen-write/cleaned_audio/clean1.mp3"

clean_audio_advanced(audio_path, output_path)
