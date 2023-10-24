from langchain.docstore.document import Document 
from langchain.llms import OpenAI
#from langchain.qa import load_qa_chain
from langchain.chains.question_answering import load_qa_chain
import json
import requests
from dotenv import load_dotenv
load_dotenv() 
import os
from pprint import pprint

openai_api_key = os.getenv("OPENAI_API_KEY")
PALM = os.getenv("PALM")
def escribirAI(transcription):

    doc = Document(page_content=transcription)
    llm = OpenAI()
    qa_chain = load_qa_chain(llm, chain_type="stuff")
    summary = qa_chain.run(input_documents=[doc],  
                      question="This is a transcription made from a customer care call at Konnect Wifi ISP , please try to summarize what is going on in English. Please note, the transcription was made using Whisper and some parts may seem hazy due to audio problems, However try as much as you can by combining all segments and figuring out. Another thing to note , being an ISP company make note of some words despite wrong spelling may be related to routers, devices, WIFI,portal and so on")
    print(summary)
    return summary

def askpalm(prompt):
    """Generates text using the Generative Language API.

    Args:
        prompt: A string containing the prompt for text generation.

    Returns:
        A string containing the generated text.
    """
    print("Calling Palmer for help!")
    headers = {'Content-Type': 'application/json'}
    data = {'prompt': {'text': prompt}}
    response = requests.post(
        f'https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText?key={PALM}',
        headers=headers,
        data=json.dumps(data))
    response.raise_for_status()

    # Parse the response as JSON
    gentext = response.json()

    # Extract the generated text from the response
    ans = gentext['candidates'][0]['output']

    return ans

# transcription = "File: segment_1.wav (Language: sw):K kFile: segment_2.wav (Language: sw):, kwa hivyo, kFile: segment_3.wav (Language: sw):Kwanzaa ni confirm, niwaneka mando inao Pana, siyo yonamba Ukona yoruta, ukona yoruta, konekti wa nyumba Namba kani hulipena kwa agent 0742257616 Pantone Wachani angalilie kuyo agent waka kujo kusaidia"
# #escribirAI(transcription)
# ans = askpalm(f"Please summarize. Here it is= '{transcription}")
# pprint(ans)