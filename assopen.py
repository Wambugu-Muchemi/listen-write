from langchain.document_loaders import AssemblyAIAudioTranscriptLoader
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
import assemblyai as aai
import dotenv
import os
from dotenv import load_dotenv
load_dotenv()
aais = os.getenv('aai')
open = os.getenv('open')

openai = OpenAI(openai_api_key=f"{open}")
aai.settings.api_key = f"{aais}"
FILE_URL = "https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"

loader = AssemblyAIAudioTranscriptLoader(FILE_URL)
docs = loader.load()

llm = OpenAI()
qa_chain = load_qa_chain(llm, chain_type="stuff")

answer = qa_chain.run(input_documents=docs,
                      question="who interrogated the professor")
print(answer)