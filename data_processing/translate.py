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
LANGUAGES_DST = CWD / "frontend" / "src" / "languages"
LANGUAGES_SRC = CWD / "data_processing" / "languages"
LOOKUP_HEADERS = {
    "Ocp-Apim-Subscription-Key": conf.TRANSLATOR_KEY,
    "Ocp-Apim-Subscription-Region": conf.TRANSLATOR_LOCATION,
    "Content-Type": "application/json",
}
LOOKUP_URL = conf.TRANSLATOR_ENDPOINT + "/dictionary/lookup"
SESSION = requests.Session()


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

    response = SESSION.post(LOOKUP_URL, params=params, headers=headers, json=body)
    result = response.json()
    # See https://docs.microsoft.com/en-us/azure/cognitive-services/translator/quickstart-translator?tabs=python#dictionary-lookup-alternate-translations
    return result


def detect_languages() -> list[Language]:
    languages = []

    # Check configuration entries
    for code, name in conf.LANGUAGES.items():
        word_file = LANGUAGES_SRC / code / "words.txt"
        dst_file = LANGUAGES_DST / code / "words.json"

        if not word_file.exists():
            logger.warning(
                "Failed to find {path} for language {lang} ({code})",
                path=word_file,
                lang=name,
                code=code,
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

    # Check for any missing from configuration
    language_paths = os.listdir(str(LANGUAGES_SRC))
    for code in language_paths:
        if conf.LANGUAGES.get(code, None) is None:
            logger.warning(
                "Found path for language {code} but no configuration", code=code
            )

    return languages


def is_translated(source, translations):
    """
    Attempt to filter out words that were not correctly translated
    """

    if not translations:
        return False

    if len(translations) == 1:
        source = source.lower()
        if source == translations[0]["word"].lower():
            return False

    return True


def process_language(language: Language):
    """
    Load the word list for the language, and existing translations.
    Put every word not yet translated through the Translation API,
    and update the word data file for frontend.
    """

    word_data: list[dict] = []
    translated_words: list[str] = []
    logger.info("Processing {lang}", lang=language.name)

    if language.dst_file.exists():
        # Read previous translations
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
        """
        Write the word data file for this language
        """
        data = orjson.dumps(word_data, option=orjson.OPT_INDENT_2)
        language.dst_file.write_bytes(data)

    def _add_translation(source, translate_results):
        """
        Process translation result to a word
        """
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
                "Failed to translate {lang} word {source}",
                lang=language.name,
                source=source,
            )
            return

        logger.info(
            "{lang} word {source} is {translations}",
            lang=language.name,
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

        # A bit excessive, but this way we save time and API calls while developing
        _write_data()

    # Loop through every word
    with language.word_file.open(encoding="utf-8") as file:
        for word in file.readlines():
            word = word.strip()
            if word == "":
                # Skip empty lines
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

            _add_translation(word, response)

    # Just in case we optimize the saves later
    _write_data()


def main():
    LANGUAGES_DST.mkdir(parents=True, exist_ok=True)

    languages = detect_languages()
    for lang in languages:
        process_language(lang)

    language_conf_data = orjson.dumps(
        [
            {
                "code": lang.code,
                "name": lang.name,
            }
            for lang in languages
        ],
        option=orjson.OPT_INDENT_2,
    )

    language_conf = LANGUAGES_DST / "languages.json"
    language_conf.write_bytes(language_conf_data)
