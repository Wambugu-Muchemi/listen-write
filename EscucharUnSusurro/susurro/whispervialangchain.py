from langchain.llms import xinference
import xinference
import whisper

# Launch Whisper model with Xinference 
model_uid = xinference.launch(model_name="whisper.en")  

# Create Xinference LLMS with Whisper model UID
llm = xinference(server_url="http://localhost:9997", model_uid=model_uid)

# Load audio file
audio = whisper.load_audio("en_example.wav") 

# Transcribe audio to text
transcription = llm.predict(audio)

print(transcription)