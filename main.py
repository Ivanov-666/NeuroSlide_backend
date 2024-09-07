# -*- coding: utf-8 -*-
import json
import os

from fastapi import Depends, FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from neuroslide.chat_tokener import Tokener
from neuroslide.plot import create_plot, read_excel_with_coordinates
from neuroslide.schemas import generateRequest, PlotData, rewriteRequest
from neuroslide.word_reader import WordFileReader
from neuroslide.writer import YaGptInference
from settings import Settings
from starlette.responses import RedirectResponse
from typing_extensions import Annotated

app = FastAPI()
settings = Settings()
tokener = Tokener(settings.YandexGPT_KEY)
chatmodel = YaGptInference()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
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
    """
    Uploads a document and processes its content for chat context.

    Args:
        chat_id (str): The identifier for the chat session.
        file (UploadFile): The uploaded Word document file.

    Returns:
        dict: A dictionary indicating the status of the upload process.
    """
    word_reader = WordFileReader()
    file_content = await file.read()

    with open(file.filename, "wb") as f:
        f.write(file_content)
    text_from_word = word_reader.read_file(file.filename)

    chatmodel.set_context(text_from_word, chat_id)
    os.remove(file.filename)

    return {"STATUS": "SUCCESS"}


@app.post("/get_base_presentation")
async def generate_complete(message: generateRequest):
    """
    Generates a base presentation based on the provided message.

    Args:
        message (generateRequest): The request object containing the message and chat ID.

    Returns:
        dict: The generated presentation text in JSON format.
    """
    token = tokener.get_token()
    presentation_text = chatmodel.get_base_presentation(
        message.message, message.chat_id, token
    )
    return json.loads(presentation_text)


@app.post("/rewrite_text")
async def rewrire_text(message: rewriteRequest):
    """
    Rewrites the provided text based on the user's request.

    Args:
        message (rewriteRequest): The request object containing the message, old text, and chat ID.

    Returns:
        str: The newly rewritten text.
    """
    token = tokener.get_token()
    new_text = chatmodel.rewrite_text(
        message.message, message.old_text, message.chat_id, token
    )
    return new_text


@app.post("/plot")
async def plot_graph(plot: Annotated[PlotData, Depends()]) -> StreamingResponse:
    x_data, y_data = read_excel_with_coordinates(
        plot.file.file,
        plot.x_start_row,
        plot.x_end_row,
        plot.x_column,
        plot.y_start_row,
        plot.y_end_row,
        plot.y_column,
    )

    img = create_plot(
        x_data,
        y_data,
        plot.chart_type,
        plot.x_bar_name,
        plot.y_bar_name,
        plot.color,
        plot.title,
    )

    return StreamingResponse(img, media_type="image/png")
