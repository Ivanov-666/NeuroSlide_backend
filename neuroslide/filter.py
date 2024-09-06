from nltk.corpus import stopwords
import nltk
from razdel import tokenize
import re

class Filter:
    def __init__(self):
        nltk.download('stopwords')
        self.stopwords = stopwords.words('russian')
    def filter_request(self, message):
        message = message.lower()
        message = re.sub('[\\r|\\n]+', ' ', message)
        message = re.sub('[a-zA-Z]+', '', message)
        message = re.sub('[0-9]+', '', message)
        message = re.sub('[^\s^\w]+', '', message)
        return " ".join([w for w in tokenize(message) if w not in stopwords])