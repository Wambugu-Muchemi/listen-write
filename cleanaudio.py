from pydub import AudioSegment

audio = AudioSegment.from_file("/home/wambugumuchemi/Projects/listen-write/audiobank/segment_1.mp3", format="mp3")
clean_audio = audio.low_pass_filter(1200).high_pass_filter(200)
# Export the processed audio to a new file
clean_audio.export("cleansegment1.mp3", format="mp3")
