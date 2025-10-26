from orjson import orjson
from rich import print
from rich.console import Console
from rich.table import Table

from data_processing.settings import LANGUAGES_DST, conf
from data_processing.utils import GenerateResponse, list_words


def get_word_data(language_id: str, word: str) -> GenerateResponse:
    ai_path = LANGUAGES_DST / f"{language_id}/ai/"
    result_file = ai_path / f"{word}.json"
    return GenerateResponse(**orjson.loads(result_file.read_text(encoding="utf-8")))


def main():
    console = Console()
    for language_id in conf.LANGUAGES:
        language = conf.LANGUAGES[language_id]

        print(f" ----- {language} -----")

        for word in sorted(list_words(language_id)):
            try:
                word_data = get_word_data(language_id, word)
                table = Table(title=word)
                table.add_column("Translation", no_wrap=True)
                table.add_column("Sentence")

                max_row = len(word_data.translation)
                if len(word_data.sentences) > max_row:
                    max_row = len(word_data.sentences)

                for row in range(max_row):
                    translation = ""
                    sentence = ""
                    if len(word_data.translation) > row:
                        translation = word_data.translation[row]
                    if len(word_data.sentences) > row:
                        sentence = word_data.sentences[row]
                    table.add_row(translation, sentence)

                console.print(table)
                print(word_data.context)
                print("")
            except Exception:  # nosec: B112:try_except_continue
                # print(e)
                continue
