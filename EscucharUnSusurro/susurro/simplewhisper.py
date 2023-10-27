import whisper

model = whisper.load_model("large")
result = model.transcribe("/home/wambugumuchemi/Projects/listen-write/only_speech.wav")
print(result["text"])