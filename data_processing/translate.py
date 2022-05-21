import os
from copy import copy
from pathlib import Path
from uuid import uuid4

import orjson
import requests
from loguru import logger
from pydantic import BaseModel

from data_processing.settings import conf

CWD = Path(".")
LOOKUP_URL = conf.TRANSLATOR_ENDPOINT + "/dictionary/lookup"
LOOKUP_HEADERS = {
    "Ocp-Apim-Subscription-Key": conf.TRANSLATOR_KEY,
    "Ocp-Apim-Subscription-Region": conf.TRANSLATOR_LOCATION,
    "Content-Type": "application/json",
}
_SESSION = requests.Session()


class Language(BaseModel):
    code: str
    name: str
    word_file: Path
    dst_file: Path


class TranslatedWord(BaseModel):
    word: str
    tag: str


class Word(BaseModel):
    source: str
    translations: list[TranslatedWord]


def get_translation(code, source) -> dict:
    headers = copy(LOOKUP_HEADERS)
    headers["X-ClientTraceId"] = str(uuid4())

    params = {
        "api-version": "3.0",
        "from": code,
        "to": "en",
    }

    body = [{"text": source}]

    response = _SESSION.post(LOOKUP_URL, params=params, headers=headers, json=body)
    result = response.json()
    # See https://docs.microsoft.com/en-us/azure/cognitive-services/translator/quickstart-translator?tabs=python#dictionary-lookup-alternate-translations
    return result


def detect_languages() -> list[Language]:
    languages = []

    for code, name in conf.LANGUAGES.items():
        word_file = CWD / "data_processing" / "languages" / code / "words.txt"
        dst_file = CWD / "frontend" / "src" / "languages" / code / "words.json"

        if not word_file.exists():
            logger.warning(
                "Failed to find {path} for language {code}", path=word_file, code=code
            )
            continue

        languages.append(
            Language(
                code=code,
                name=name,
                word_file=word_file,
                dst_file=dst_file,
            )
        )

    language_paths = os.listdir(str(CWD / "data_processing" / "languages"))
    for code in language_paths:
        if conf.LANGUAGES.get(code, None) is None:
            logger.warning(
                "Found path for language {code} but no configuration", code=code
            )

    return languages


def is_translated(source, translations):
    if not translations:
        return False

    if len(translations) == 1:
        source = source.lower()
        if source == translations[0]["word"].lower():
            return False

    return True


def process_language(language: Language):
    logger.info("Processing language {code}", code=language.code)
    word_data: list[dict] = []
    translated_words: list[str] = []

    if language.dst_file.exists():
        _word_data = orjson.loads(language.dst_file.read_bytes())
        logger.info("Found existing translations at {path}", path=language.dst_file)

        for word in _word_data:
            if not is_translated(word["source"], word["translations"]):
                continue

            word_data.append(word)
            translated_words.append(word["source"])
    else:
        # Ensure parent path exists
        language.dst_file.parent.mkdir(parents=True, exist_ok=True)

    def _write_data():
        data = orjson.dumps(word_data, option=orjson.OPT_INDENT_2)
        language.dst_file.write_bytes(data)

    def _add_word(source, translate_results):
        translations = []
        for translate_result in translate_results:
            for translation in translate_result["translations"]:
                translations.append(
                    {
                        "word": translation["displayTarget"],
                        "tag": translation["posTag"],
                    }
                )

        if not is_translated(source, translations):
            logger.warning(
                "Failed to translate {code} word {source}",
                code=language.code,
                source=source,
            )
            return

        logger.info(
            "{code} word {source} is {translations}",
            code=language.code,
            source=source,
            translations=translations,
        )

        translated_words.append(source)
        word_data.append(
            Word(
                source=source,
                translations=[
                    TranslatedWord(
                        word=word["word"],
                        tag=word["tag"],
                    )
                    for word in translations
                ],
            ).dict()
        )

        _write_data()

    with language.word_file.open(encoding="utf-8") as file:
        for word in file.readlines():
            word = word.strip()
            if word == "":
                continue

            if word in translated_words:
                logger.debug(
                    "Word {word} is already translated, skipping...", word=word
                )
                continue

            response = get_translation(
                code=language.code,
                source=word,
            )

            _add_word(word, response)

    _write_data()


def main():
    languages = detect_languages()
    for lang in languages:
        process_language(lang)
