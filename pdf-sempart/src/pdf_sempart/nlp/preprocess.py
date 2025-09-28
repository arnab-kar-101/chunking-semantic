import re
import unicodedata

def tokens_for(text: str):
    text = text.lower()
    text = unicodedata.normalize('NFKD', text)
    text = re.sub(r'[^a-z0-9 ]+', ' ', text)
    tokens = text.split()
    return tokens
