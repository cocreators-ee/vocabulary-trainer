from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    TRANSLATOR_ENDPOINT: str = "https://api.cognitive.microsofttranslator.com/"
    TRANSLATOR_LOCATION: str = "global"
    TRANSLATOR_KEY: Optional[str] = Field(None)

    LANGUAGES: dict[str, str] = {
        "et": "Estonian",
        "fi": "Finnish",
    }

    OPENAI_PROVIDER: str = "http://127.0.0.1:1234/v1"  # E.g. locally hosted LM Studio
    # OPENAI_GENERATE_MODEL: str = "llama-3.3-70b-instruct"
    OPENAI_GENERATE_MODEL: str = "gemma-3-27b-it@q4_k_m"
    OPENAI_ANALYZE_MODEL: Optional[str] = "gemma-3-27b-it@q4_k_m"
    OPENAI_API_KEY: str = ""


conf = Config()
CWD = Path(".")
LANGUAGES_DST = CWD / "frontend" / "src" / "languages"
LANGUAGES_SRC = CWD / "data_processing" / "languages"
