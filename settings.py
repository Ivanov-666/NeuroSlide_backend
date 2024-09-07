# -*- coding: utf-8 -*-
from pydantic_settings import BaseSettings


class EnvSettings(BaseSettings):
    """
    Configuration class for environment settings.

    Attributes:
        ENV_FILE (str): The path to the environment file. Defaults to "envs/key.env".
    """

    ENV_FILE: str = "envs/key.env"


class Settings(BaseSettings):
    """
    Application settings class for managing configuration values.

    Attributes:
        YandexGPT_KEY (str): The API key for Yandex GPT. Defaults to an empty string.
        Redis_host (str): Redis server host.
        Redis_port (int): Redis server port.
        Redis_db (int): Redis db name.
        Redis_password (str): Password for redis db.

    Configuration:
        The class uses the `Config` inner class to specify the environment file from which
        to load the settings.
    """

    YandexGPT_KEY: str = ""
    Redis_host: str = ("localhost",)
    Redis_port: int = (6379,)
    Redis_db: int = (0,)
    Redis_password: str = ("neuroslide",)

    class Config:
        """
        Configuration settings for the Settings class.
        """

        env_file = EnvSettings().ENV_FILE
