from typing import Optional

from openai import AsyncOpenAI
from orjson import orjson
from pydantic_ai import Agent, UnexpectedModelBehavior, format_as_xml, ModelSettings
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers import Provider
from pydantic_ai.providers.openai import OpenAIProvider

from data_processing.settings import LANGUAGES_DST, conf
from data_processing.utils import AnalyzeResponse, GenerateResponse

GENERATE_PROMPT = """
You are a translator and interpreter. Your job is to provide useful analysis and explanations in English for words in another language to help students learn the meaning and use of the words.

IMPORTANT:
- The source language is specified in the data, make sure you use that information and instead of assuming words are in e.g. English when they look like English words.
- Provide a list of English language words the word in the source language can be translated to.
- Give 3 example sentences with the word in the given source language. Make sure the word is used at least once in the exact form given, but it's useful to have multiple forms shown as well.
- If you do not understand the word or your confidence is very low, make sure you indicate that by reporting it as not understood instead of making up an answer.
- The source of the words is mostly from movie subtitles, so there may be names of people and terms in other languages mixed in, make sure you flag those as not understood in the source language as well.
- It is important to represent the results accurately even if the word is crude in nature or in poor taste, as this date is used for educational purposes. However in the English version, the most offensive slurs should be avoided, e.g. you should use "n-word" instead of the actual word it refers to.
- Give a brief explanation in English of the word's meaning and usage as context for the students. Take into consideration the form of the word, and the different cases for words.
- You should explain the obvious components of the words, like when "ga" is used in Estonian word "õunaga" for "with", or how "mme" in the Finnish word "juhlamme" means "our". Make sure you consider when the word is e.g. in plural form and include an explanation of that and what it means for the analysis.
- Use full and complete sentences in English for your responses, without placeholders, ellipsis or similar to indicate missing information.
- You may be provided the result of previous analysis to consider when making your suggestion. They may help you understand the word in context, however they are not always correct so make sure to consider the validity of the previous translation attempt.
- You will be provided dictionary definitions when available, you should strongly consider them.
- If a dictionary is labeled as being "manual", then that is some hand-written corrections to previous data and should take priority.
"""

ANALYZE_PROMPT = """
I have a list of words provided in a given source language. Each of those words have been provided English language translations, example sentences in the source language, and some English language context explaining the use of the word.

Please analyze the answer, and confirm if it has correctly identified the source language of the word as the given language, and provided relevant and valid answers to that word. Confirm the source word is used in the exact form given in at least one of the example sentences.

We want to identify words which have a significantly invalid translation, examples, or context provided so we can re-process them. The data is used for educational purposes so it is important that you do not make mistakes, and will flag all invalid information.

You will be provided dictionary definitions when available, you should strongly consider them when evaluating the answer.
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
        api_key=conf.OPENAI_API_KEY,
        base_url=conf.OPENAI_PROVIDER,
    )
    return OpenAIChatModel(model, provider=provider, settings=ModelSettings(parallel_tool_calls=False))


def is_word_defined(language_id: str, word: str) -> bool:
    ai_path = LANGUAGES_DST / f"{language_id}/ai/"
    result_file = ai_path / f"{word}.json"
    return result_file.exists()


def has_good_analysis(language_id: str, word: str, definitions: dict, agent: Agent) -> bool:
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


def get_word_data(language_id: str, word: str) -> GenerateResponse:
    ai_path = LANGUAGES_DST / f"{language_id}/ai/"
    result_file = ai_path / f"{word}.json"
    return GenerateResponse(**orjson.loads(result_file.read_text(encoding="utf-8")))
