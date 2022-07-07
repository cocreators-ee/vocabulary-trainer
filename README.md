# Vocabulary Trainer

Tool to practice the vocabulary in a foreign language.

- [User Interface design](https://miro.com/app/board/uXjVO0rdlRk=/?share_link_id=630009358943)
- [Overall architecture](https://miro.com/app/board/uXjVO0r-ICc=/?share_link_id=733906777704)

## Development

Dependencies for development:

- [NodeJS 16 LTS](https://nodejs.org/en/)
- [Pnpm](https://pnpm.io/installation)
- [Python >= 3.8](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)
- [pre-commit](https://pre-commit.com/#install)

After checking out locally, run in the folder:

```bash
pre-commit install
```

## Data processing (optional)

When you add new languages or words and need them automatically processed via the
Translation API, you can use the data processing tooling.

To run the language data processing you will need the following environment variables
set:

- `TRANSLATOR_KEY`: The access key to your Azure Translator resource

To get the key set up your resource as per the guidance at
https://docs.microsoft.com/en-us/azure/cognitive-services/translator/quickstart-translator?tabs=python#prerequisites

Once that is set up, you can run it:

```bash
poetry install
poetry run translate
```

This will generate `frontend/src/languages/languages.json` and
`frontend/src/languages/*/words.json` for configured languages.

Language configuration is stored in `data_processing/settings.py` and source word lists
in `data_processing/languages/*/words.txt` - the word lists must be in UTF-8 encoding,
one word / phrase per line.
