import logging
import spacy
from langchain.tools import Tool

_logger = logging.getLogger(__name__)
_nlp = None


def get_nlp():
    global _nlp
    if _nlp is not None:
        return _nlp
    try:
        _nlp = spacy.load("en_core_web_sm")
    except OSError:
        _logger.warning(
            "spaCy model 'en_core_web_sm' not found. Falling back to a blank English model. "
            "To install the model run: python -m spacy download en_core_web_sm"
        )
        _nlp = spacy.blank("en")
    return _nlp


def get_entity_tool():
    def extract(text: str):
        nlp = get_nlp()
        return list({ent.text for ent in nlp(text).ents})

    return Tool(
        name="EntityExtractor",
        func=extract,
        description="Extracts named entities (people, places, etc.) from a story."
    )
