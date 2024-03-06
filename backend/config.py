from pydantic_settings import BaseSettings, SettingsConfigDict

from ai.model import EmojiClassifierConfig


class Config(BaseSettings):
    classifier: EmojiClassifierConfig = EmojiClassifierConfig()
    model_name: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="_",
    )


config = Config()
