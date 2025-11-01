from time import perf_counter

from rich import print

from data_processing.ai import get_ai_analyze_agent, has_good_analysis
from data_processing.dictionary import get_word_definitions
from data_processing.settings import conf
from data_processing.utils import list_words


def main():
    agent = get_ai_analyze_agent()
    total_start = perf_counter()
    processed_words = 0

    try:
        for language_id in conf.LANGUAGES:
            language = conf.LANGUAGES[language_id]
            print(f" ----- {language} -----")
            print("")

            for word in list_words(language_id):
                start = perf_counter()
                print(f"{word} ", end="")
                definitions = get_word_definitions(word, language_id)
                valid = has_good_analysis(language_id, word, definitions, agent)
                elapsed = perf_counter() - start

                if valid:
                    print(f"is valid ({elapsed:.3f}s)")
                else:
                    print(f"is BAD! 😢 ({elapsed:.3f}s)")

                processed_words += 1

            print("")
    except KeyboardInterrupt:
        print("Aborting...")
        pass

    total_elapsed = perf_counter() - total_start
    per_word = total_elapsed / processed_words

    print(
        f"Processed {processed_words:,} words in {total_elapsed:.3f}s, took on average {per_word:.3f}s per word."
    )
