from pathlib import Path
from typing import Optional
from urllib.parse import urljoin, urlparse, parse_qsl, urlencode, urlunparse

import bs4
import requests
from bs4 import BeautifulSoup, PageElement, NavigableString, Tag

from data_processing.settings import LANGUAGES_SRC, conf
from data_processing.utils import retry

NO_RESULTS = "No definition found in dictionary."
USER_AGENT = "curl/8.16.0"
DEBUG = False


def html_to_text(content):
    """
    Creates a formatted text email message as a string from a rendered html template (page)
    https://gist.github.com/racitup/2ded9c06c2563049e7e12b25bf2a8369
    """
    text = []
    for element in content.descendants:
        # We use type and not isinstance since comments, cdata, etc are subclasses that we don't want
        if type(element) == NavigableString:
            parent_tags = (t for t in element.parents if type(t) == Tag)
            hidden = False
            for parent_tag in parent_tags:
                # Ignore any text inside a non-displayed tag
                # We also behave is if scripting is enabled (noscript is ignored)
                # The list of non-displayed tags and attributes from the W3C specs:
                if (parent_tag.name in ('area', 'base', 'basefont', 'datalist', 'head', 'link',
                                        'meta', 'noembed', 'noframes', 'param', 'rp', 'script',
                                        'source', 'style', 'template', 'track', 'title', 'noscript') or
                    parent_tag.has_attr('hidden') or
                    (parent_tag.name == 'input' and parent_tag.get('type') == 'hidden')):
                    hidden = True
                    break
            if hidden:
                continue

            # remove any multiple and leading/trailing whitespace
            string = ' '.join(element.string.split())
            if string:
                if element.parent.name == 'a':
                    a_tag = element.parent
                    # replace link text with the link
                    string = a_tag['href']
                    # concatenate with any non-empty immediately previous string
                    if (type(a_tag.previous_sibling) == NavigableString and
                        a_tag.previous_sibling.string.strip()):
                        text[-1] = text[-1] + ' ' + string
                        continue
                elif element.previous_sibling and element.previous_sibling.name == 'a':
                    text[-1] = text[-1] + ' ' + string
                    continue
                elif element.parent.name == 'p':
                    # Add extra paragraph formatting newline
                    string = '\n' + string
                text += [string]
    doc = '\n'.join(text)
    return doc


def fetch_html(url: str) -> Optional[BeautifulSoup]:
    content = None
    content_bypass = Path(".") / "response.txt"

    if DEBUG:
        if content_bypass.exists():
            content = content_bypass.read_text()
            print(f"Reading {url} from file.")

    if not content:
        response = requests.get(url, headers={
            "User-Agent": USER_AGENT,
            "Accept": "*/*",
        })

        if response.status_code != 200:
            return None
        if not response.headers.get("content-type").startswith("text/html"):
            return None
        response.encoding = "utf-8"
        content = response.text
        if DEBUG:
            content_bypass.write_text(content, encoding="utf-8")

    return BeautifulSoup(content, "html.parser")


def word_cache_path(word, language_id, dictionary) -> Path:
    dictionary_path = LANGUAGES_SRC / language_id / dictionary
    dictionary_path.mkdir(parents=True, exist_ok=True)
    return dictionary_path / f"{word}.txt"


def cache_word(word, language_id, dictionary, contents: str):
    word_cache = word_cache_path(word, language_id, dictionary)
    word_cache.write_text(contents)


def get_word_cache(word, language_id, dictionary) -> Optional[str]:
    word_cache = word_cache_path(word, language_id, dictionary)
    if word_cache.exists():
        return word_cache.read_text()
    return None


def cleanup_html(container: BeautifulSoup | PageElement):
    # Generic HTML cleanup that is always applicable
    for link in container.find_all("a"):
        link.unwrap()

    for element in container.descendants:
        element_type = type(element)
        # Remove comments
        if element_type == bs4.element.Comment:
            element.extract()
            continue

        if element_type != bs4.element.Tag:
            continue

        if element.has_attr("src"):
            del element["src"]
        if element.has_attr("width"):
            del element["width"]
        if element.has_attr("height"):
            del element["height"]
        if element.has_attr("id"):
            del element["id"]
        if element.has_attr("data-accel-col"):
            del element["data-accel-col"]
        if element.has_attr("colspan"):
            del element["colspan"]
        if element.has_attr("rowspan"):
            del element["rowspan"]
        if element.has_attr("class"):
            del element["class"]
        if element.has_attr("style"):
            del element["style"]


@retry
def ekss(word, language_id) -> Optional[str]:
    """
    Estonian dictionary
    https://arhiiv.eki.ee/dict/ekss/
    """
    # Construct the URL
    url_parts = urlparse("https://arhiiv.eki.ee/dict/ekss/index.cgi?F=M")
    query = dict(parse_qsl(url_parts.query))
    query.update({"Q": word})
    url = urlunparse(url_parts._replace(query=urlencode(query)))

    content = fetch_html(url)

    if content is None:
        return NO_RESULTS

    answer = content.select_one(".tervikart")
    if answer is None:
        return NO_RESULTS

    # Find any data about "redirects"
    previous_p = [
        p
        for p in answer.previous_siblings
        if type(p) == bs4.element.Tag and p.name == "p"
    ]

    replacement = [
        p
        for p in previous_p
        if "Asendasin" in p.text
    ]

    # Include the information at the top
    for element in replacement:
        answer.insert(0, element)

    cleanup_html(answer)
    answer.smooth()
    return html_to_text(answer)

def wiktionary(word, language_id) -> Optional[str]:
    """
    Multilingual wiki based dictionary
    https://wiktionary.org/
    """
    language = conf.LANGUAGES[language_id]
    url = urljoin("https://en.wiktionary.org/wiki/", word)
    content = fetch_html(url)

    if content is None:
        return NO_RESULTS

    try:
        header = f"h2#{language}"
        heading_block = content.select_one(header).parent

        # Remove previous siblings before heading
        for elem in heading_block.previous_siblings:
            elem.extract()

        # Check if we can find another language heading, if so remove that and everything after it
        remove = False
        for elem in heading_block.next_siblings:
            if remove:
                elem.extract()
            if type(elem) == bs4.element.Tag:
                if elem.has_attr("class") and "mw-heading2" in elem["class"]:
                    remove = True
                    elem.extract()

        container = heading_block.parent
    except AttributeError:
        return NO_RESULTS

    for element in container.select("mw-editsection"):
        element.extract()

    # Remove "Further reading"
    further_reading = container.select_one("[id^='Further_reading']")
    if further_reading:
        cont = further_reading.parent
        ul = cont.next_sibling
        while type(ul) != bs4.element.Tag or ul.name != "ul":
            ul = ul.next_sibling

        ul.extract()
        cont.extract()

    # Remove "Anagrams"
    anagrams = container.select_one("[id^='Anagrams']")
    if anagrams:
        cont = anagrams.parent
        ul = cont.next_sibling
        while type(ul) != bs4.element.Tag or ul.name != "ul":
            ul = ul.next_sibling

        ul.extract()
        cont.extract()

    cleanup_html(container)
    container.smooth()
    container.name = "div"
    text = html_to_text(container)
    text = text.replace("[\nedit\n]\n", "")
    return text


def manual_information(word, language_id) -> Optional[str]:
    manual_dictionary = LANGUAGES_SRC / language_id / "manual"
    manual_dictionary.mkdir(parents=True, exist_ok=True)
    word_cache = manual_dictionary / f"{word}.txt"
    if word_cache.exists():
        return word_cache.read_text()
    return None


LANGUAGE_DICTS = {
    "fi": [wiktionary],
    "et": [ekss, wiktionary],
}


def get_word_definitions(word, language_id) -> dict[str, str]:
    """
    Find data from all the available dictionaries for the word, using local caching when possible to avoid
    unnecessary traffic on their servers.
    """
    result = {}
    dictionaries = LANGUAGE_DICTS[language_id]

    for dict_func in dictionaries:
        dict_name = dict_func.__name__
        answer = get_word_cache(word, language_id, dict_name)
        if answer is None:
            answer = dict_func(word, language_id)
            if answer is None:
                raise Exception(f"Failed to get {language_id} dictionary definition for {word} from {dict_name}")
            cache_word(word, language_id, dict_name, answer)
        result[dict_name] = answer

    manual = manual_information(word, language_id)
    if manual:
        result["manual"] = manual

    return result
