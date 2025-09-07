import re

def normalize(text):
    # remove emotes
    text = re.sub(r':\_[^:]+:', ' ', text)
    text.replace(' ', '')

    text = text.lower()
    # remove symbols, special characters
    text = re.sub(r'[^\w\s]', '', text) 
    return text.strip()