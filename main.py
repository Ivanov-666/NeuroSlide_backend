import os
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from dotenv import load_dotenv
from fantasium.text_to_speech import TtsModel
from fantasium.chat_tokener import Tokener
from fantasium.schemas import Message
from fantasium.illustrator import Text2ImageAPI
from fantasium.transcriber import Transcriber
from fantasium.writer import GigachatInference
from fantasium.filter import Filter
from settings import Settings

app = FastAPI()
settings = Settings()
tokener = Tokener(settings.Gigachat_KEY)
ttsmodel = TtsModel()
chatmodel = GigachatInference(settings.Story_len)
transcribe = Transcriber()
filter = Filter()
image_api = Text2ImageAPI('https://api-key.fusionbrain.ai/', settings.Kandinsky_API_KEY, settings.Kandinsky_SECRET_KEY)
model_id = image_api.get_model()

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
def generate_complete(message: Message):
    #message = filter.filter_request(message)
    token = tokener.get_token()
    story_content, end_of_story = chatmodel.get_text(message.message, message.chat_id, token)
    audio_data = ttsmodel.get_audio(story_content)

    return {
        "story": story_content,
        "end_of_story": end_of_story,
        "transcription": audio_data,
    }

@app.post("/illustrator")
def send_illustator(model: Message):
    uuid = image_api.generate(model.message, model_id)
    images = image_api.check_generation(uuid)

    return {"image": images[0]}


@app.post('/transcribe')
async def upload_file(file: UploadFile = File()):
    context = await file.read()

    with open('temp_file.wav', 'wb') as temp_file:
        temp_file.write(context)
        result = transcribe.process('temp_file.wav')

    return {"transcription": result}
