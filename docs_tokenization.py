# Gelin Eguinosa Rosique

import spacy
from spacy.util import compile_infix_regex
from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER, CONCAT_QUOTES, LIST_ELLIPSES, LIST_ICONS

import pickle
from os import mkdir
from os.path import isdir, isfile, join


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


def corpus_tokenization(documents, from_scratch=True, data_dir='data', file_name='tokens.pickle'):
    """
    Receives the texts from the documents in the corpus and creates, and
    transforms each document into an array of tokens.
    Removes all the stop words, punctuation symbols and numbers in the
    documents, lowercases the text and lemmatizes each token.
    :param documents: An iterable sequence containing the texts of the documents
    in the corpus.
    :param from_scratch: Bool to determine if we used a previously calculated
    tokenization of the corpus, or if we start from scratch, even though we have
    the result of the tokenization saved.
    :param data_dir: The folder where the data of the project is saved.
    :param file_name: The name of the file where the tokens are or will be saved.
    :return: The list of tokens for each of the documents in the corpus.
    """
    # Check if the folder 'data' exists, and in case the folder doesn't exist
    # create it.
    if not isdir(data_dir):
        mkdir(data_dir)

    # The Location of the tokens:
    tokens_path = join(data_dir, file_name)

    # Check if the user wants to use the saved tokens and the tokens are
    # saved.
    if not from_scratch:
        if not isfile(tokens_path):
            raise Exception("There are no tokens information saved for this"
                            "corpus.")
        # We use pickle to save and load the tokens.
        with open(tokens_path, 'rb') as file:
            corpus_tokens = pickle.load(file)
        return corpus_tokens

    # Creating a list of lists containing the tokens of the documents
    corpus_tokens = list(lazy_corpus_tokenization(documents))

    # Save the tokens of the corpus in a file:
    with open(tokens_path, 'wb') as file:
        pickle.dump(corpus_tokens, file)

    return corpus_tokens


def saved_tokenization(data_dir='data', file_name='tokens.pickle'):
    """
    Check if the tokens from a previous tokenization process where saved so you
    can use this data without going through all the tokenization again.
    :param data_dir: The folder where the data of the project is saved.
    :param file_name: The name of the file where the tokens are or will be saved.
    :return: A bool representing if the tokens for the corpus are saved or not.
    """
    # Create the full path of the tokens file
    tokens_path = join(data_dir, file_name)
    # Check if the tokens exist
    result = isfile(tokens_path)
    return result


def docs_tokenization(documents):
    """
    A simple tokenization process.
    Receive the texts of all the documents in the corpus, and transform each
    text into an array of tokens.
    Removes all the stop words, punctuation symbols and numbers in the
    documents, lowercases the text and lemmatizes each token.
    :param documents: A sequence of the texts of all the documents in the corpus.
    :return: A list of tokens for each document.
    """
    # Loading the English Package
    nlp = spacy.load('en_core_web_md')

    # List containing the tokens per each document in the corpus
    docs_tokens = []

    # Iterate through the text of the documents and return their tokens
    for text in documents:
        text_doc = nlp(text, disable=['ner', 'textcat'])
        text_tokens = [token.lemma_.lower().strip()
                       for token in text_doc
                       if token.is_alpha and not token.is_stop]
        docs_tokens.append(text_tokens)

    return docs_tokens


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
