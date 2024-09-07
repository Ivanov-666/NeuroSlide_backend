from nltk.corpus import stopwords
import nltk
from razdel import tokenize
import re

class Filter:
    """
    A class to filter and preprocess text messages.

    Attributes:
        stopwords (list): A list of Russian stopwords used for filtering.
    """

    def __init__(self):
        """
        Initializes the Filter class and downloads the necessary stopwords.
        """
        nltk.download('stopwords')
        self.stopwords = stopwords.words('russian')
    def filter_request(self, message):
        """
        Filters the input message by removing stopwords, numbers, and special characters.
        
        Args:
            message (str): The input message to be filtered.

        Returns:
            str: The filtered message with stopwords and unwanted characters removed.
        """
        message = message.lower()
        message = re.sub('[\\r|\\n]+', ' ', message)
        message = re.sub('[a-zA-Z]+', '', message)
        message = re.sub('[0-9]+', '', message)
        message = re.sub('[^\s^\w]+', '', message)
        return " ".join([w for w in tokenize(message) if w not in stopwords])