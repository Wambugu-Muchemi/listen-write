import re

def clean_repeated_text(segment_text):
    """
    Remove repeated words and phrases from the input segment text.

    Args:
    - segment_text: The input text.

    Returns:
    - The cleaned text with repeated words and phrases removed.
    """
    pattern = re.compile(r"(.+)(\1{2,})", re.IGNORECASE)

    if re.search(pattern, segment_text):
        matches = re.findall(pattern, segment_text)
        cleaned_text = re.sub(pattern, r'\1', segment_text)
        return cleaned_text
    else:
        return segment_text

def read_and_clean_text(input_file_path, output_file_path):
    """
    Read text from an input file, clean it by removing repeated words and phrases, and write the cleaned text to an output file.

    Args:
    - input_file_path: The path to the input text file.
    - output_file_path: The path to the output text file.
    """
    with open(input_file_path, 'r') as file:
        segment_text = file.read()
        cleaned_text = clean_repeated_text(segment_text)

    with open(output_file_path, 'w') as file:
        file.write(cleaned_text)

# Example usage
# input_file_path = './audiokon.txt'
# output_file_path = './audiokonclean.txt'
# read_and_clean_text(input_file_path, output_file_path)