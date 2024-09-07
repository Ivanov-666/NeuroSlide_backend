import os
import json
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from neuroslide.word_reader import WordFileReader
from neuroslide.chat_tokener import Tokener
from neuroslide.schemas import generateRequest, rewriteRequest
from neuroslide.writer import GigachatInference
from neuroslide.filter import Filter
from settings import Settings

app = FastAPI()
settings = Settings()
tokener = Tokener(settings.Gigachat_KEY)
chatmodel = GigachatInference(settings.Story_len)
filter = Filter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)


# Redirect / -> Swagger-UI documentation
@app.get("/")
def main_function():
    """
    # Redirect
    to documentation (`/docs/`).
    """
    return RedirectResponse(url="/docs/")

@app.post("/upload_doc")
async def generate_complete(chat_id: str, file: UploadFile = File(...)):
    word_reader = WordFileReader()
    file_content = await file.read()

    with open(file.filename, 'wb') as f:
        f.write(file_content)
    text_from_word = word_reader.read_file(file.filename)

    chatmodel.set_context(text_from_word, chat_id)
    os.remove(file.filename)
    
    return {
        "STATUS": "SUCCESS"
    }

@app.post("/get_base_presentation")
async def generate_complete(message: generateRequest):
    token = tokener.get_token()
    presentation_text = chatmodel.get_base_presentation(message.message, message.chat_id, token)

    return json.loads(presentation_text)

@app.post("/rewrite_text")
async def rewrire_text(message: rewriteRequest):
    token = tokener.get_token()
    new_text = chatmodel.rewrite_text(message.message, message.old_text, message.chat_id, token)
    return new_text
