from pydantic_settings import BaseSettings
class EnvSettings(BaseSettings):
    ENV_FILE: str = "envs/key.env"
 

class Settings(BaseSettings):
    YandexGPT_KEY: str = ''

    class Config:
        env_file = EnvSettings().ENV_FILE
