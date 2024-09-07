from pydantic import BaseModel

class generateRequest(BaseModel):
    message: str
    chat_id: str

class rewriteRequest(BaseModel):
    message: str
    old_text: str
    chat_id: str