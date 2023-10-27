import whisper

model = whisper.load_model("large")
result = model.transcribe("./only_speech.wav")
print(result["text"])