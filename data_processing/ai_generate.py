import sys
from time import perf_counter

from pydantic_ai import UnexpectedModelBehavior, format_as_xml
from rich import print
from tqdm import tqdm

from data_processing.ai import (
    get_ai_analyze_agent,
    get_ai_generate_agent,
    has_good_analysis,
)
from data_processing.settings import LANGUAGES_DST, conf
from data_processing.utils import GenerateResponse, list_words


def print_output(elapsed: float, output: GenerateResponse):
    understood = "understood" if output.understood else "NOT understood"
    print(f"({elapsed:.3f}s) (confidence {output.confidence:.2f}, {understood})")
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
    if "--check" in sys.argv[1]:
        check = True
        analysis_agent = get_ai_analyze_agent()

    if "--verbose" in sys.argv[1]:
        verbose = True

    total_start = perf_counter()
    total_words = 0
    processed_words = 0
    reprocessed = 0

    for language_id in conf.LANGUAGES:
        language = conf.LANGUAGES[language_id]
        print(f" ----- {language} -----")
        print("")
        word_progress = tqdm(list(list_words(language_id)), colour="green")
        for word in word_progress:
            word_progress.set_description(f"{word:<24}")
            reprocessing = False
            total_words += 1
            while True:
                try:
                    word_prop = "word_in_" + language.lower()
                    request = {
                        "source_language": language,
                        "source_language_id": language_id,
                        word_prop: word,
                    }

                    prompt = format_as_xml(request, root_tag="user")

                    if verbose:
                        print(f"{word} ", end="")

                    if is_word_defined(language_id, word):
                        if not check:
                            if verbose:
                                print("... skipping")
                            break

                        if has_good_analysis(language_id, word, analysis_agent):
                            if verbose:
                                print("... skipping")
                            break
                        else:
                            reprocessing = True

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

    total_elapsed = perf_counter() - total_start
    per_word = total_elapsed / processed_words

    print(
        f"Processed {processed_words:,} words in {total_elapsed:.1f}s, took on average {per_word:.1f}s per word."
    )

    if check:
        reprocessed_pct = (reprocessed / total_words) * 100
        print(
            f"{reprocessed_pct:.1f}% of the words were missing or needed reprocessing."
        )
