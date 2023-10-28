from celery import Celery

#create a celery app instance
app = Celery('audioTask', broker='redis://localhost:6379/5')

#this is the function to transcribe
@app.task
def transcribe_audio(audio_file_url):
    #TODO: Implement audio processing here
    return print("processing audio {}".format(audio_file_url))


