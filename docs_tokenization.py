# Gelin Eguinosa Rosique

import spacy
from spacy.util import compile_infix_regex
from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER, CONCAT_QUOTES, LIST_ELLIPSES, LIST_ICONS


def lazy_corpus_tokenization(documents):
    """
    Does the tokenization of the corpus in a lazy fashion, one document at a
    time, when the document is needed.
    Removes all the stop words, punctuation symbols and numbers in the
    documents, lowercases the text and lemmatizes each token.
    :param documents: An iterable sequence containing the texts of the documents
    in the corpus.
    :return: The sequence of the tokens of the documents in the corpus in a lazy
    fashion.
    """
    # Tokenization of the corpus:
    # Loading the English Package
    nlp = spacy.load('en_core_web_md')

    # Changing the infixes to accept words with hyphens (-), like 'covid-19'
    infixes = (
            LIST_ELLIPSES
            + LIST_ICONS
            + [
                r"(?<=[0-9])[+\-\*^](?=[0-9-])",
                r"(?<=[{al}{q}])\.(?=[{au}{q}])".format(
                    al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES
                ),
                r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
                # r"(?<=[{a}])(?:{h})(?=[{a}])".format(a=ALPHA, h=HYPHENS),
                r"(?<=[{a}0-9])[:<>=/](?=[{a}])".format(a=ALPHA),
            ]
    )
    infix_re = compile_infix_regex(infixes)
    nlp.tokenizer.infix_finditer = infix_re.finditer

    # Iterating through the text of the documents and doing the tokenization
    for text in documents:
        # Disable 'ner' and 'textcat' for faster processing
        text_doc = nlp(text, disable=['ner', 'texcat'])

        # Lemmatize the tokens, lower the characters, and take only the tokens
        # with at least one alphabetic character. (food, covid-19, R2, etc..)
        text_tokens = [token.lemma_.lower().strip()
                       for token in text_doc
                       if len(token.text) > 1
                       and ((token.is_alpha and not token.is_stop)
                       or (not token.is_alpha and is_acceptable(token.text)))]
        # Returns one tokenized document at a time.
        yield text_tokens


def is_acceptable(text):
    """
    Checks if a text only contains alphabetic or numeric characters, or hyphens
    (-). The needs to have at least one alphabetic character to be acceptable.
    :param text: The text we need to check
    :return: A bool representing if the text contains only alphabetic
    characters and hyphens or not.
    """
    # To see check if it has at least one alphabetic character and hyphen:
    has_alpha = False
    has_hyphen = False
    for char in text:
        # If it's not alphabetic, numeric or a hyphen, not a valid word
        if not (char.isalpha() or char.isnumeric()) and char != '-':
            return False
        if char.isalpha():
            has_alpha = True
        if char == '-':
            has_hyphen = True
    return has_alpha and has_hyphen
