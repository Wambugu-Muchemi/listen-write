import re
from pprint import pprint

def clean_repeated_text(segment_text):
    # Define a regular expression pattern for repeated text
    #pattern = re.compile(r'(\b\w+\b)(?:.*\b\1\b){3,}', re.IGNORECASE)
    pattern = re.compile(r"(.+)(\1{2,})", re.IGNORECASE)

    # Check if the segment text contains repetitions
    if re.search(pattern, segment_text):
        # Find all repeated patterns in the segment text
        matches = re.findall(pattern, segment_text)

        # Remove the repetitions from the segment text
        cleaned_text = re.sub(pattern, r'\1', segment_text)

        return cleaned_text
    else:
        return segment_text

def readtxtfile():
    file_path = './audiokon.txt'

    # Read the content of the file into the segment_text variable
    with open(file_path, 'r') as file:
        segment_text = file.read()
        # Clean the segment text by removing repeated words and phrases
        cleaned_text = clean_repeated_text(segment_text)
        print("Cleaned Text:\n",cleaned_text)
        with open('./audiokonclean.txt', 'w') as file:
            file.write(cleaned_text)
    

# Example usage
# segment_text = "Kwa hivyo, kwa hivyo, kwa hivyo, kwa hivyo, "
# cleaned_text = clean_repeated_text(segment_text)
# print("Original Text:", segment_text)
# print("Cleaned Text:", cleaned_text)
#readtxtfile()
