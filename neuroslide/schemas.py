from pydantic import BaseModel

class generateRequest(BaseModel):
    """
    A model representing a request to generate a presentation.

    Attributes:
        message (str): The message content provided by the user for generating the presentation.
        chat_id (str): The unique identifier for the chat session associated with the request.
    """
    message: str
    chat_id: str

class rewriteRequest(BaseModel):
    """
    A model representing a request to rewrite text.

    Attributes:
        message (str): The message content provided by the user for rewriting.
        old_text (str): The original text that needs to be rewritten.
        chat_id (str): The unique identifier for the chat session associated with the request.
    """
    message: str
    old_text: str
    chat_id: str