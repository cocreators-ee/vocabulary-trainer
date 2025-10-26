from typing import Optional

from openai import AsyncOpenAI
from orjson import orjson
from pydantic_ai import Agent, UnexpectedModelBehavior, format_as_xml
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers import Provider
from pydantic_ai.providers.openai import OpenAIProvider

from data_processing.settings import LANGUAGES_DST, conf
from data_processing.utils import AnalyzeResponse, GenerateResponse

GENERATE_PROMPT = """
I need you to provide context and translations for common words in a given language. You need to translate the word into English, and give 3 example sentences with the word in the source language, preferably using different forms of the same word.

If you do not know the answer, do not make one up. The results will be used to teach others the source language, so it's important that they are not misled. Give an accurate confidence rating to your answers, and don't be afraid to flag any words you don't understand.

The source of the words is mostly from movie subtitles, so there may be names of people and terms in other languages mixed in, and we want to filter those out from the results as well.

It is important to represent the results accurately even if the word is crude in nature or in poor taste, as this date is used for educational purposes.

Also give a context for the word's meaning or usage in English, explaining shortly how it is commonly used.

Use full and complete sentences in English for your responses, do not leave in placeholders, ellipsis or similar to indicate missing information.

Do not make mistakes.

The source word is always in the source language, not in English even if it is similar to an English word.
"""

ANALYZE_PROMPT = """
I have a list of words provided in a given source language. Each of those words have been provided English language translations, example sentences in the source language, and some English language context explaining the use of the word.

Please analyze the answer, and confirm if it has correctly identified the source language of the word as the given language, and provided relevant and valid answers to that word.

We want to identify words which have a significantly invalid translation, examples, or context provided so we can re-process them. The data is used for educational purposes so it is important that you do not make mistakes, and will flag all invalid information.
"""


def _make_analysis_prompt(language_id: str, word):
    language = conf.LANGUAGES[language_id]

    ai_path = LANGUAGES_DST / f"{language_id}/ai/"
    ai_path.mkdir(parents=True, exist_ok=True)

    result_file = ai_path / f"{word}.json"
    result = GenerateResponse(**orjson.loads(result_file.read_text()))

    prompt = {
        f"word_in_{language.lower()}": word,
        "translations_in_english": result.translation,
        f"example_sentences_in_{language.lower()}": result.sentences,
        "context": result.context,
    }

    return format_as_xml(prompt, root_tag="user")


def _get_ai_model(model: Optional[str] = None) -> OpenAIChatModel:
    if model is None:
        model = conf.OPENAI_GENERATE_MODEL
    provider: Provider[AsyncOpenAI] = OpenAIProvider(
        api_key=conf.OPENAI_API_KEY, base_url=conf.OPENAI_PROVIDER
    )
    return OpenAIChatModel(model, provider=provider)


def is_word_defined(language_id: str, word: str) -> bool:
    ai_path = LANGUAGES_DST / f"{language_id}/ai/"
    result_file = ai_path / f"{word}.json"
    return result_file.exists()


def has_good_analysis(language_id: str, word: str, agent: Agent) -> bool:
    while True:
        try:
            if not is_word_defined(language_id, word):
                return False

            prompt = _make_analysis_prompt(language_id, word)
            result = agent.run_sync(prompt)
            output: AnalyzeResponse = result.output

            return output.valid
        except UnexpectedModelBehavior:
            print("Error, retrying...")


def get_ai_generate_agent() -> Agent:
    model = _get_ai_model()
    return Agent(model, instructions=GENERATE_PROMPT, output_type=GenerateResponse)


def get_ai_analyze_agent() -> Agent:
    model = _get_ai_model(conf.OPENAI_ANALYZE_MODEL)
    return Agent(model, instructions=ANALYZE_PROMPT, output_type=AnalyzeResponse)
