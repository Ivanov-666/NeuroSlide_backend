import os
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from neuroslide.word_reader import WordFileReader
from dotenv import load_dotenv
from neuroslide.chat_tokener import Tokener
from neuroslide.schemas import Message
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

@app.post("/generate_complete")
async def generate_complete(file: UploadFile = File(...)):
    word_reader = WordFileReader()
    file_content = await file.read()

    with open(file.filename, 'wb') as f:
        f.write(file_content)
    text_from_word = word_reader.read_file(file.filename)
    
    token = tokener.get_token()
    story_content, end_of_story = chatmodel.get_text(text_from_word, "1", token)

    os.remove(file.filename)

    return {
        "story": story_content,
        "end_of_story": end_of_story
    }