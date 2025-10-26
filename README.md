# Vocabulary Trainer

Tool to practice the vocabulary in a foreign language.

- [User Interface design](https://miro.com/app/board/uXjVO0rdlRk=/?share_link_id=630009358943)
- [Overall architecture](https://miro.com/app/board/uXjVO0r-ICc=/?share_link_id=733906777704)

## Development

Dependencies for development:

- [NodeJS 22 LTS](https://nodejs.org/en/)
- [Pnpm](https://pnpm.io/installation)
- [Python >= 3.13](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)
- [pre-commit](https://pre-commit.com/#install)

After checking out locally, run in the folder:

```bash
pre-commit install
```

## Frontend

To work on the frontend, you will need to install the dependencies and then run the `dev` script:

```bash
cd frontend
pnpm install
pnpm run dev
```

## Data processing (optional)

### Machine translation

When you add new languages or words and need them automatically processed via the Translation API, you can use
the data processing tooling.

To run the language data processing you will need the following environment variables set:

- `TRANSLATOR_KEY`: The access key to your Azure Translator resource

To get the key set up your resource as per the guidance at
https://docs.microsoft.com/en-us/azure/cognitive-services/translator/quickstart-translator?tabs=python#prerequisites

Once that is set up, you can run it:

```bash
poetry install
poetry run translate
```

This will generate `frontend/src/languages/languages.json` and `frontend/src/languages/*/words.json` for
configured languages.

Language configuration is stored in [data_processing/settings.py](.data_processing/settings.py) and source
word lists in `data_processing/languages/*/words.txt` - the word lists must be in UTF-8 encoding, one word /
phrase per line.

### AI analysis

It may be helpful to provide some automatic AI generated analysis of the words as well, even with all the
caveats. For that we have some utilities.

Requirements:

- Access to OpenAI compatible API, e.g. via locally hosted LM Studio
- Suitable model for generating answers, e.g. `qwen3-32b@q4_k_m`, `llama-3.3-70b-instruct@q4_k_m`, or
  `gemma-3-27b-it@q4_k_m`
- Configure the `OPENAI_*` parameters in [data_processing/settings.py](.data_processing/settings.py)

Then you can run the utilities:

```bash
# To generate AI analysis for words missing one
poetry run ai_generate
```

```bash
# To include words where the model believes the previous answer to be invalid
poetry run ai_generate --check
```

```bash
# To use AI to review AI analysis
poetry run ai_analyze
```

```bash
# To manually review the AI analysis results for the words
poetry run review_ai
```

Keep in mind all the AI tools are likely to run fairly slowly on a local machine, depending on your hardware
and model. They might take a minute or two per word, or maybe just 10 seconds, and we have about 10,000 words
to process in total. With a model that does not run well on your hardware you may be committing to many days
of execution time.


# Financial support

This project has been made possible thanks to [Cocreators](https://cocreators.ee) and [Lietu](https://lietu.net). You
can help us continue our open source work by supporting us
on [Buy me a coffee](https://www.buymeacoffee.com/cocreators).

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/cocreators)
