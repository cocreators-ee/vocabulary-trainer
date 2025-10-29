from pydantic import BaseModel, Field

from data_processing.settings import LANGUAGES_SRC


class GenerateResponse(BaseModel):
    understood: bool = Field(
        description="You comprehend this word, and it is a word in the source language."
    )
    sentences: list[str] = Field(
        description="List of example sentences in the source language using the word in different forms."
    )
    translation: list[str] = Field(
        description="List of words and phrases in English that have the same or very similar meaning"
    )
    context: str = Field(
        description="A short explanation of the meaning or usage of the word in plain English."
    )


class AnalyzeResponse(BaseModel):
    valid: bool = Field(
        description="The translations, examples, and provided context are not significantly incorrect."
    )


def list_words(language_id: str):
    with (LANGUAGES_SRC / f"{language_id}/words.txt").open() as f:
        for word in f.readlines():
            yield word.strip()
