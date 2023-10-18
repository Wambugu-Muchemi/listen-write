from transformers import WhisperProcessor, WhisperForConditionalGeneration
import dotenv
import os
dotenv.load_dotenv()
hugtoken = os.environ.get("HUGGINGFACE")
token = hugtoken

model_name = "openai/whisper-tiny-en"
processor = WhisperProcessor.from_pretrained(model_name)
model = WhisperForConditionalGeneration.from_pretrained(model_name)

model.config.forced_decoder_ids = processor.get_decoder_prompt_ids(language = "en", task = "transcribe")
input_features = processor(speech, sampling_rate=16000, return_tensors="pt").input_features 
predicted_ids = model.generate(input_features, max_length=448)
transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)