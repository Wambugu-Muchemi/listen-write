import pickle
import whisper

def picklenow():
    # Load the model
    model = whisper.load_model("large-v2")

    # Save the model to a pickle file
    with open("whisper_model.pkl", "wb") as file:
        pickle.dump(model, file)

