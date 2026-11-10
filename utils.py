import re

def clean_text(text):
    #remove html tags
    text=re.sub(r'<.*?>', '', text)
    #remove urls
    text=re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    # remove special characters and numbers
    text=re.sub(r'[^a-zA-Z0-9 ]', '', text)
    # replace multiple spaces with a single space
    text=re.sub(r'\s{2,}', ' ', text)
    # trivm leading and trailing spaces
    text=text.strip()
    # remove extra whitespace
    text=' '.join(text.split())
    return text
