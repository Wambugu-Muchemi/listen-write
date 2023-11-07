from langchain.docstore.document import Document 
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
import json
import requests
from dotenv import load_dotenv
import os
from pprint import pprint

load_dotenv() 
openai_api_key = os.getenv("OPENAI_API_KEY")
PALM = os.getenv("PALM")

def escribir_AI(transcription):
    """
    Generate a summary and issue category from a transcription.

    Args:
    - transcription: The transcription text.

    Returns:
    - A tuple containing the summary and issue category.
    """
    doc = Document(page_content=transcription)
    llm = OpenAI()
    qa_chain = load_qa_chain(llm, chain_type="stuff")

    summary = qa_chain.run(
        input_documents=[doc],
        question="This is a transcription made from a customer care call at Konnect Wifi which is an ISP company, please try to summarize what is going on in English. Please note, the transcription was made using Whisper and some parts may seem hazy due to audio problems, However try as much as you can by combining all segments and figuring out. Another thing to note, being an ISP company make note of some words despite wrong spelling may be related to routers (whisper keeps pronouncing router as 'ruta' so if you see ruta know its router), devices, WIFI, portal and so on"
    )

    issue_category = ask_palm(f"{summary} Categorize this summary as any of the following: Router Installation, Change / Add Device, Product Enquiry, TV Connection, SMS Code Issue, Payment Issue, Router Technical Problem, Obtaining IP Issue, Connection Speed Issue, Login Challenge or Other")

    print(issue_category)
    print(summary)
    return summary, issue_category

def ask_palm(prompt):
    """
    Generates text using the Generative Language API.

    Args:
        prompt: A string containing the prompt for text generation.

    Returns:
        A string containing the generated text.
    """
    print("Calling Palmer for help!")

    headers = {'Content-Type': 'application/json'}
    data = {'prompt': {'text': prompt}}

    try:
        response = requests.post(
            f'https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText?key={PALM}',
            headers=headers,
            data=json.dumps(data)
        )
        response.raise_for_status()

        # Parse the response as JSON
        gentext = response.json()

        # Extract the generated text from the response
        ans = gentext['candidates'][0]['output']
        return ans

    except requests.exceptions.RequestException as e:
        print(f"Error calling Palmer API: {e}")
        return ''