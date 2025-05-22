from pydantic_settings import BaseSettings

class QwenSettings(BaseSettings):
    DASHSCOPE_API_KEY: str = "sk-08e9ac76a3874c5faef20e67ac8f60d7"
    MODEL_NAME: str = "qwen-max"
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 1500
    TOP_P: float = 0.8
    
    class Config:
        env_file = ".env"
    