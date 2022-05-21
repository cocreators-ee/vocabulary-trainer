from pydantic import BaseSettings, Field


class Config(BaseSettings):
    TRANSLATOR_ENDPOINT: str = "https://api.cognitive.microsofttranslator.com/"
    TRANSLATOR_LOCATION: str = "global"
    TRANSLATOR_KEY: str = Field(...)

    LANGUAGES = {
        "et": "Estonian",
        "fi": "Finnish",
    }


conf = Config()
