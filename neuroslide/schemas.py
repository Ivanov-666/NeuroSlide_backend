# -*- coding: utf-8 -*-
from fastapi import File, UploadFile
from pydantic import BaseModel, Field


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


class PlotData(BaseModel):
    file: UploadFile = File(...)
    chart_type: str = Field(default="line", alias="lineBarScatter")
    x_start_row: int = Field(...)
    x_end_row: int = Field(...)
    x_column: int = Field(...)
    y_start_row: int = Field(...)
    y_end_row: int = Field(...)
    y_column: int = Field(...)
    x_bar_name: str = Field("Время")
    y_bar_name: str = Field("Деньги")
    color: str = Field("blue")  # #fff тут тоже робит
    title: str = Field("Plot")
