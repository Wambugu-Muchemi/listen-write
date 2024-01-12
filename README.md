# EscucharUnSusurro: Advanced Audio Transcription and Inferential Analysis Toolkit

![EscucharUnSusurro Logo](EscucharUnSusurro/susurro/compressedlogo2.jpeg)

## Overview

EscucharUnSusurro is a powerful toolkit designed for audio transcription and in-depth inferencing analysis. Leveraging cutting-edge technologies such as Whisper ASR (Automatic Speech Recognition), Silero VAD (Voice Activity Detection), and AI language models like GPT-3 and Google Palm APIs, this project transforms raw audio into valuable insights. I coined the name EscucharUnSusurro from Spanish *Escuchar un sussuro* meaning 'Listen to a Whisper', symbolizing the nuanced inferencing capabilities embedded within each sound.

## Key Features

### 1. Whisper ASR Integration

- **Whisper Accuracy:** EscucharUnSusurro utilizes the advanced Whisper ASR (Automatic Speech Recognition) model, renowned for its exceptional accuracy in transcribing audio content. This integration ensures that the toolkit delivers highly precise and reliable transcriptions for a wide range of audio inputs.

  - **Model Loading:** The Whisper ASR model is loaded into the toolkit, allowing it to perform real-time transcription on audio files.

  - **Preprocessing:** Before transcription, the audio is preprocessed by padding or trimming to fit a standardized 30-second duration. This ensures consistency in the input format for optimal performance.

  - **Log-Mel Spectrogram:** The Whisper model works with log-Mel spectrograms, a representation of the audio signal that captures its frequency content over time. This spectrogram is created from the preprocessed audio and is moved to the same device as the model.

  - **Language Detection:** The Whisper model is equipped to detect the spoken language within the audio, providing valuable information about the linguistic context.

  - **Transcription:** The Whisper ASR model decodes the log-Mel spectrogram, generating a transcription result. The transcribed text is then accessible for further analysis or storage.

  - **Usage Example:**
    ```python
    from whisper import load_model, load_audio, log_mel_spectrogram, pad_or_trim, decode

    # Load the Whisper ASR model
    model = load_model("large-v2")

    # Load audio file
    audio_path = "path/to/your/audio/file.wav"
    audio = load_audio(audio_path)

    # Preprocess audio (pad/trim to fit 30 seconds)
    audio = pad_or_trim(audio)

    # Create log-Mel spectrogram
    mel = log_mel_spectrogram(audio).to(model.device)

    # Decode the audio
    result = decode(model, mel)

    # Get the transcription
    transcription = result.text
    print("Transcription:", transcription)
    ```
  - This example demonstrates how to transcribe an audio file using the Whisper ASR model and extract the resulting transcription for further use. Note: If your audio content is purely in English, you could change `large-v2` model to `tiny` or `base` as they are English-only models thus tend to perform better and faster.
  
### 2. Silero VAD Implementation

- **Efficient Preprocessing:** EscucharUnSusurro integrates Silero VAD (Voice Activity Detection) to enhance the efficiency of audio preprocessing. Silero VAD specializes in identifying voice activity within an audio stream, allowing the toolkit to focus on relevant speech segments and discard non-speech portions.

  - **VAD Initialization:** Silero VAD is initialized with the chosen device (CPU or GPU) to process the audio stream effectively.

  - **Raw PCM Data Processing:** The audio is converted to raw PCM (Pulse Code Modulation) data, and Silero VAD applies its voice activity detection algorithm to distinguish speech from silence.

  - **Silencing Non-Speech Segments:** Silero VAD identifies non-speech segments and removes them from the audio, resulting in a cleaned version optimized for subsequent analysis.

  - **Dynamic Application:** Silero VAD adapts dynamically to varying audio conditions, making it suitable for different environments and speech patterns.

  - **Usage Example:**

    ```python
    """
      Args:
      - audiopath: The path to the input audio file.

      Returns:
      - The path to the VAD-processed audio file.
    """
      SAMPLING_RATE = 16000
      
      try:
          import librosa
          audio, sr = librosa.load(audiopath, sr=None)
      except Exception as e:
          print(f"Error loading audio file: {e}")
          return 'no silero'

      if sr != SAMPLING_RATE:
          print("Warning: Original audio samplerate differs from expected 16kHz.\n\tOriginal SamplingRate: ", sr)
          audio = librosa.resample(audio, orig_sr=sr, target_sr=SAMPLING_RATE)

      AUDIO_FILENAME = "temp_audio.wav"
      librosa.output.write_wav(AUDIO_FILENAME, audio, SAMPLING_RATE)

      try:
          model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad', force_reload=True)
          (get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks) = utils

          wav = read_audio(AUDIO_FILENAME, sampling_rate=SAMPLING_RATE)
          
          speech_timestamps = get_speech_timestamps(wav, model, sampling_rate=SAMPLING_RATE)
          save_audio('only_speech.wav', collect_chunks(speech_timestamps, wav), sampling_rate=SAMPLING_RATE)
          
          return 'only_speech.wav'
      except Exception as e:
          print(f"Error processing audio with Silero VAD: {e}")
          import os
          if os.path.exists(AUDIO_FILENAME):
              os.remove(AUDIO_FILENAME)
          if os.path.exists('only_speech.wav'):
              os.rename('only_speech.wav', 'no_silero.wav')
          return 'no silero'
    ```
  OR
    ```python
    # Sample code for voice activity detection using Silero VAD
    from silero import Vad

    # Initialize Silero VAD
    vad = Vad(device='cpu')  # Use 'cuda' if you have a GPU

    # Process audio file
    input_audio_path = "path/to/your/audio/file.wav"
    output_audio_path = "path/to/your/output/cleaned_audio.wav"

    # Apply VAD to the raw PCM data
    vad.process_audio(input_audio_path, output_audio_path)
    ```
  - The provided example demonstrates how to utilize Silero VAD to process an audio file, removing non-speech segments and creating a cleaned version ready for further analysis.


### 3. Intelligent Segmentation

- **Enhanced Processing:** EscucharUnSusurro incorporates an intelligent segmentation process to optimize the handling of audio streams. This technique involves breaking down the audio stream into segments, offering several advantages for efficient parallel processing and reducing the overall computational load.

  - **Segmentation Algorithm:** The toolkit employs a segmentation algorithm to identify logical breakpoints within the audio stream. These breakpoints are strategically chosen to maintain the integrity of speech segments while facilitating parallel processing.

  - **Parallelization Benefits:** Segmentation enables parallel processing of smaller audio chunks, harnessing the full potential of multi-core systems and distributed computing environments. This results in faster overall processing times, especially for large audio files.

  - **Dynamic Duration Configuration:** Users can configure the duration of each segment based on their specific requirements. This flexibility allows adaptation to varying audio content and processing goals.

  - **Usage Example:**
    ```python
      from pydub import AudioSegment
      import os

      def split_audio(input_file, output_folder, segment_duration=25):
          print("Segmenting...")
          audio = AudioSegment.from_file(input_file)

          # Calculate the number of segments
          num_segments = len(audio) // (segment_duration * 1000)
          print(f"{num_segments} segments found.")

          for i in range(num_segments):
              start_time = i * segment_duration * 1000
              end_time = (i + 1) * segment_duration * 1000

              # Extract the segment
              segment = audio[start_time:end_time]

              # Save the segment in WAV format
              output_file = f"{output_folder}/segment_{i + 1}.wav"
              segment.export(output_file, format="wav")
              print(f"{output_file} processed.")

          # Handle the last segment
          last_segment = audio[num_segments * segment_duration * 1000:]
          if len(last_segment) > 0:
              output_file = f"{output_folder}/segment_{num_segments + 1}.wav"
              last_segment.export(output_file, format="wav")
    ```
    Then
    
    ```python
    # Sample code for audio segmentation
    from segmenter import split_audio

    # Segment audio file with 25-second duration
    input_audio_path = "path/to/your/audio/file.wav"
    output_folder = "path/to/your/output/segments"
    split_audio(input_audio_path, output_folder, segment_duration=25)
    ```
  - The provided example showcases how to use the segmentation function to break down an audio file into segments with a specified duration. Adjust the segment duration parameter based on your processing needs.


### 4. AI-Powered Analysis

- **GPT-3 Integration:** EscucharUnSusurro integrates the OpenAI GPT-3 API, a powerful language model, to enhance natural language understanding and extract context-aware insights from transcribed audio content.

  - **Versatile Language Understanding:** GPT-3 is capable of understanding and generating human-like text, making it a valuable tool for analyzing and summarizing the transcriptions obtained from Whisper ASR.

  - **Context-Aware Summarization:** The toolkit leverages GPT-3 to generate concise summaries of transcribed content, providing a condensed yet informative overview of the spoken words.

- **Google Palm APIs:** EscucharUnSusurro utilizes Google Palm APIs to complement the analysis with additional context and semantic insights.

  - **Enhanced Context Analysis:** Google Palm APIs offer advanced context analysis, helping the toolkit extract nuanced information related to the content, such as detecting key topics, entities, and relationships.

  - **Semantic Understanding:** The integration with Palm APIs enriches the toolkit's semantic understanding capabilities, allowing it to identify and categorize relevant information within the transcriptions.

  - **Usage Example:**
    ```python
    # Sample code for GPT-3 analysis
    from langchain.docstore.document import Document 
    from langchain.llms import OpenAI
    from langchain.chains.question_answering import load_qa_chain

    # Load GPT-3 and related components
    llm = OpenAI()
    qa_chain = load_qa_chain(llm, chain_type="stuff")

    # Sample document for analysis
    document = Document(page_content="Transcription content goes here.")

    # Run GPT-3 analysis
    summary = qa_chain.run(input_documents=[document], question="Summarize this transcription.")
    print("GPT-3 Summary:", summary)
    ```
  - This example demonstrates how to leverage GPT-3 for summarizing transcribed content, providing a quick and insightful overview.

  - **Note:** Ensure proper API key configuration for both GPT-3 and Google Palm APIs to enable seamless integration. There is no limitation to use either LLM to leverage the summary generation. I just used both to showcase both implementations.


### 5. SQLite Database Management

- **Structured Data Storage:** EscucharUnSusurro employs the SQLite database management system for organized storage and retrieval of transcribed information. This relational database ensures a structured and efficient way to store large volumes of data generated during the transcription and analysis process.

  - **Table Structure:** The toolkit creates a dedicated table within the SQLite database to store transcriptions. This table is designed with specific fields, including date, source URL, transcription, summary, issue category, and customer contact, providing a comprehensive and organized storage structure.

  - **Data Integrity:** SQLite ensures data integrity by enforcing constraints, relationships, and transactions, preventing data corruption and ensuring the accuracy of stored information.

  - **Data Retrieval:** Users can easily query the SQLite database to retrieve specific information based on criteria such as date, source URL, or issue category, facilitating targeted analysis.

- **Data Deduction:** Extracted insights from transcribed audio content are systematically cataloged within the SQLite database for streamlined access and analysis.

  - **Cataloging Process:** The toolkit automatically catalogs key insights, including transcriptions, summaries, issue categories, and contact information, allowing users to efficiently navigate and explore the extracted information.

  - **Querying for Insights:** Users can query the database to retrieve relevant insights, enabling in-depth analysis, trend identification, and report generation based on the stored data.

  - **Usage Example:**
    ```python
    # Sample code for storing transcriptions in SQLite
    from storage import store_transcription_in_sqlite

    # Example data
    source_url = "https://example.com/audio1"
    transcription = "Transcribed content goes here."
    date = "2023-11-04 15:30:00"
    summary = "GPT-3 generated summary of the transcription."
    issue_category = "Technical Support"
    contact = "customer@example.com" #Note: You can also use phone number

    # Store transcription in SQLite
    store_transcription_in_sqlite(source_url, transcription, date, summary, issue_category, contact)
    ```
  - The provided example demonstrates how to store a transcription in the SQLite database, including relevant metadata. Adjust the input parameters based on your specific data.


### 6. Data Visualization

- **Matplotlib, Seaborn, Plotly:** EscucharUnSusurro leverages powerful data visualization tools, including Matplotlib, Seaborn, and Plotly, to create clear and informative visual representations of transcribed data.

  - **Matplotlib:** A versatile plotting library that allows for the creation of a wide range of static visualizations, including bar charts, line plots, and histograms. It is well-suited for detailed exploration of data trends.

  - **Seaborn:** Built on top of Matplotlib, Seaborn specializes in statistical data visualization. It enhances the aesthetic appeal of visualizations and provides additional plotting functions for complex datasets.

  - **Plotly:** Offers interactive and dynamic charts, enabling users to explore trends and patterns in a more engaging manner. Plotly supports various chart types, such as scatter plots, line charts, and choropleth maps.

- **Dynamic Charts:** EscucharUnSusurro provides dynamic and interactive charts, enhancing the user experience and facilitating exploration of insights within the transcribed data.

  - **Folium Integration:** The toolkit utilizes Folium, a Python wrapper for Leaflet.js, to create interactive maps. For example, geographical data related to calls from contacts can be visualized on an interactive map, providing spatial context.

  - **KML Files:** Keyhole Markup Language (KML) files can be generated to visualize geographical data in platforms like Google Earth, offering a comprehensive view of call locations.

  - **Pie Charts:** Visualizing the distribution of issue categories can be achieved through dynamic pie charts, allowing users to quickly grasp the proportion of different types of issues.

  - **Usage Example:**
    ```python
    # Sample code for dynamic charts and maps
    import matplotlib.pyplot as plt
    import seaborn as sns
    import plotly.express as px
    import folium
    from visualize import create_pie_chart, create_folium_map, create_kml_file

    # Example data retrieval from SQLite
    # (Assuming the necessary queries and data fetching functions are available)

    # Create a pie chart for issue categories
    create_pie_chart(data)

    # Create an interactive map using Folium
    create_folium_map(geographical_data)

    # Create a KML file for Google Earth
    create_kml_file(geographical_data)
    ```
  - This example illustrates how to use Matplotlib, Seaborn, Plotly, Folium, and KML files to visualize different aspects of transcribed data. Modify the functions based on the specific visualizations you want to generate. See these examples on google colab;
  
  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Wambugu-Muchemi/listen-write/blob/main/EscucharUnSusurro/susurro/colabstatusfromdb.ipynb)


### 7. Whisper Model Optimization

- **Pickling Whisper Model:** EscucharUnSusurro incorporates model optimization techniques by pickling the Whisper ASR model. Pickling involves serializing the model and saving it to a file, allowing for efficient storage and faster execution.

  - **Speed Enhancement:** Pickling the Whisper model significantly improves the speed of model loading compared to loading it directly from the original source. This optimization is especially beneficial in scenarios where quick model loading is crucial for real-time or resource-intensive applications.

  - **CPU Intensity Observation:** During testing, it was noted that loading the model directly from the pickled file was more CPU-intensive compared to loading from the source. Pickling serves as a performance optimization strategy, reducing the computational overhead associated with loading the model.

  - **Usage Consideration:** While pickling enhances speed, it's essential to consider the trade-off with disk space. Pickled models consume additional storage, and users should balance the advantages of faster loading times with the available storage capacity.

  - **Usage Example:**
    ```python
    # Sample code for pickling the Whisper model
    """
    Load the Whisper model and save it to a pickle file.
    """
    # Load the model
    model = whisper.load_model("large-v2")

    # Save the model to a pickle file
    with open("whisper_model.pkl", "wb") as file:
        pickle.dump(model, file)
    ```
  - This example demonstrates how to pickle the Whisper model for optimization. Run this process periodically or when necessary to ensure the most up-to-date pickled model is available for faster loading.

  - **Note:** Ensure that sufficient disk space is available, and monitor the trade-off between storage usage and loading speed based on the specific requirements of your application.


## Getting Started

1. **Installation:**

   To get started with EscucharUnSusurro, follow these steps:

   - Clone the repository to your local machine:

     ```bash
     git clone https://github.com/Wambugu-Muchemi/listen-write.git
     ```

   - Create a virtual environment and navigate to the project directory:

     ```bash
     cd EscucharUnSusurro/susurro
     ```

   - Install the required dependencies using pip:

     ```bash
     pip install -r requirements.txt
     ```

   This will ensure that all the necessary libraries and modules are installed for running the EscucharUnSusurro workflow.

2. **Run the Workflow:**

   - Execute the main workflow script `segmentedwhisper.py`:

     ```bash
     python segmentedwhisper.py
     ```

   - Follow the on-screen prompts to enter the transcription URL and customer contact information.

   - The workflow will process the audio, transcribe, clean, summarize with AI, and store the results in an SQLite database.

   Congratulations! You have successfully run the EscucharUnSusurro workflow. Adjustments to the workflow or additional configurations can be made based on specific use cases or requirements.

## `Acknowledgements`

This project is built upon the remarkable work of the [OpenAI Whisper](https://github.com/openai/whisper) team. Whisper is an advanced Automatic Speech Recognition (ASR) model developed by OpenAI, and its capabilities form the foundation of EscucharUnSusurro.

Please check out the official [OpenAI Whisper repository](https://github.com/openai/whisper) for detailed information on the Whisper ASR model, usage guidelines, and updates from the OpenAI team.

**Note:** Make sure to review and comply with the licensing and attribution requirements specified by the original project.





