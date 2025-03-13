import re
import spacy
'''
def split_concatenated_words(text):
    """Splits concatenated words in a sentence (e.g., camelCase, PascalCase)."""
    if not isinstance(text, str):
        return text
    return re.sub(r'([a-z])([A-Z])', r'\1 \2', text)


nlp=spacy.load("en_core_web_sm", disable=["parser","ner"])
nlp.add_pipe('sentencizer')
def split_sentences(text):
    doc = nlp(text)
    return " ".join([sent.text for sent in doc.sents])'''
import wordninja

def split_sentences(text):
    if not isinstance(text, str):  
        return text  # Skip non-string values
    return " ".join(wordninja.split(text))  # Split concatenated words


