import pickle
import whisper

def picklenow():
    """
    Load the Whisper model and save it to a pickle file.
    """
    # Load the model
    model = whisper.load_model("large")

    # Save the model to a pickle file
    with open("whisper_model.pkl", "wb") as file:
        pickle.dump(model, file)

# Example usage
# pickle_model()

