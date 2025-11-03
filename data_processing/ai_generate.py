import sys
from time import perf_counter

from pydantic_ai import UnexpectedModelBehavior, format_as_xml
from rich import print
from tqdm import tqdm

from data_processing.ai import (
    get_ai_analyze_agent,
    get_ai_generate_agent,
    has_good_analysis, get_word_data,
)
from data_processing.dictionary import get_word_definitions
from data_processing.settings import LANGUAGES_DST, conf
from data_processing.utils import GenerateResponse, list_words


def print_output(elapsed: float, output: GenerateResponse):
    understood = "understood" if output.understood else "NOT understood"
    print(f"({elapsed:.3f}s) ({understood})")
    if output.understood:
        print("In English: " + "; ".join(output.translation))
        print("")
        print("Example sentences:")
        for sentence in output.sentences:
            print(f" - {sentence}")
        print("")
        print(output.context)
        print("")


def is_word_defined(language_id: str, word: str) -> bool:
    ai_path = LANGUAGES_DST / f"{language_id}/ai/"
    result_file = ai_path / f"{word}.json"
    return result_file.exists()


def write_result(language_id: str, word, output: GenerateResponse):
    ai_path = LANGUAGES_DST / f"{language_id}/ai/"
    ai_path.mkdir(parents=True, exist_ok=True)

    result_file = ai_path / f"{word}.json"
    with open(result_file, "tw") as f:
        f.write(output.model_dump_json(indent=2))


def main():
    agent = get_ai_generate_agent()
    analysis_agent = None

    verbose = False
    check = False
    regenerate = False
    skip = 0
    skip_until = None
    languages = conf.LANGUAGES
    language_words = {
        lang: list_words(lang)
        for lang in conf.LANGUAGES
    }

    if "--check" in sys.argv:
        check = True
        analysis_agent = get_ai_analyze_agent()

    if "--regenerate" in sys.argv:
        regenerate = True

    if "--verbose" in sys.argv:
        verbose = True

    if "--skip" in sys.argv:
        skip_idx = sys.argv.index("--skip") + 1
        skip = int(sys.argv[skip_idx])

    if "--skip-until" in sys.argv:
        skip_until_idx = sys.argv.index("--skip-until") + 1
        skip_until = sys.argv[skip_until_idx]

    if "--language" in sys.argv:
        language_idx = sys.argv.index("--language") + 1
        languages = [sys.argv[language_idx]]

    if "--word" in sys.argv:
        word_idx = sys.argv.index("--word") + 1
        language_words = {
            lang: [sys.argv[word_idx]]
            for lang in conf.LANGUAGES
        }

    total_start = perf_counter()
    total_words = 0
    processed_words = 0
    reprocessed = 0

    try:
        for language_id in languages:
            language = conf.LANGUAGES[language_id]
            print(f" ----- {language} -----")
            print("")

            word_list = list(language_words[language_id])
            skip_words = min(len(word_list), skip)
            word_list = word_list[skip_words:]
            skip -= skip_words
            smoothing = 1 if skip_until else 0.05

            word_progress = tqdm(word_list, colour="green", smoothing=smoothing)
            for word in word_progress:
                if skip_until:
                    if word == skip_until:
                        skip_until = False
                    else:
                        continue
                else:
                    word_progress.smoothing = 0.05

                word_progress.set_description(f"{word:<24}")
                reprocessing = False
                total_words += 1
                definitions = get_word_definitions(word, language_id)

                while True:
                    try:
                        word_prop = "word_in_" + language.lower()
                        request = {
                            "source_language": language,
                            "source_language_id": language_id,
                            word_prop: word,
                            "dictionary_definitions": definitions
                        }

                        prompt = format_as_xml(request, root_tag="user")

                        if verbose:
                            print(f"{word} ", end="")

                        if is_word_defined(language_id, word):
                            if regenerate:
                                request["previous_analysis"] = get_word_data(language_id, word).model_dump()
                            elif not check:
                                if verbose:
                                    print("... exists")
                                break
                            elif has_good_analysis(language_id, word, definitions, analysis_agent):
                                if verbose:
                                    print("... good enough")
                                break
                            else:
                                reprocessing = True
                                request["previous_analysis"] = get_word_data(language_id, word).model_dump()

                        start = perf_counter()
                        result = agent.run_sync(prompt)
                        elapsed = perf_counter() - start

                        if verbose:
                            print_output(elapsed, result.output)
                        if result.output.understood:
                            write_result(language_id, word, result.output)

                        processed_words += 1
                        if reprocessing:
                            reprocessed += 1
                        break
                    except UnexpectedModelBehavior:
                        if verbose:
                            print("Error, retrying...")

            print("")
    except KeyboardInterrupt:
        print("Aborting...")
        pass

    total_elapsed = perf_counter() - total_start
    per_word = total_elapsed / max(processed_words, 1)
    processed_pct = processed_words / max(total_words, 1)

    print(
        f"Processed {processed_words:,} ({processed_pct:.1f}%) words "
        f"in {total_elapsed:.1f}s, "
        f"took on average {per_word:.1f}s per word."
    )

    if check:
        reprocessed_pct = (reprocessed / total_words) * 100
        print(
            f"{reprocessed_pct:.1f}% of the words were missing or needed reprocessing."
        )
