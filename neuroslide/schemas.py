# -*- coding: utf-8 -*-
from fastapi import File, UploadFile
from pydantic import BaseModel, Field


class generateRequest(BaseModel):
    message: str
    chat_id: str


class rewriteRequest(BaseModel):
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
