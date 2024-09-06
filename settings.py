from pydantic_settings import BaseSettings
class EnvSettings(BaseSettings):
    ENV_FILE: str = "envs/key.env"
 

class Settings(BaseSettings):
    Gigachat_KEY: str = ''
    Kandinsky_API_KEY: str = ''
    Kandinsky_SECRET_KEY: str = ''
    Story_len: int = 5

    class Config:
        env_file = EnvSettings().ENV_FILE
