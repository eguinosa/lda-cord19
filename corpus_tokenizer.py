# Gelin Eguinosa Rosique

import json
from os import mkdir
from os.path import isdir, isfile, join
from gensim.models import Phrases

from docs_tokenization import lazy_corpus_tokenization


class CorpusTokenizer:
    """
    Class to tokenize the documents of a corpus and save the results in case
    they are needed later.
    """
    # Location Class Data
    data_folder = 'project_data'
    tokens_folder = 'docs_tokenized'
    tokens_prefix = 'doc_tokens_'
    tokenization_index_name = 'tokenization_index.json'

    def __init__(self, documents, _use_saved=False):
        """
        Receives the texts from the documents in the corpus and creates, and
        transforms each document into an array of tokens.
        Removes all the stop words, punctuation symbols and numbers in the
        documents, lowercases the text and lemmatizes each token.
        :param documents: An iterable sequence containing the texts of the
        documents in the corpus.
        :param _use_saved: Bool to determine if we used a previously generated
        tokenization of the corpus, or if we start from scratch, even if we have
        the result of the tokenization saved.
        """
        # The path of the folder for the tokenized documents.
        tokens_folder_path = join(self.data_folder, self.tokens_folder)

        # Create data folder if it doesn't exist.
        if not isdir(self.data_folder):
            mkdir(self.data_folder)

        # Create tokens folder if it doesn't exist.
        if not isdir(tokens_folder_path):
            mkdir(tokens_folder_path)

        # Check if the user wants to use the saved tokens
        if _use_saved:
            index_path = join(tokens_folder_path, self.tokenization_index_name)
            # Check if we saved the tokens for this corpus
            if not isfile(index_path):
                raise Exception("No tokens previously saved for this corpus.")
            # Load the tokens information from the index file:
            with open(index_path, 'r') as file:
                self.tokens_info = json.load(file)

        # Do the tokenization of the documents
        else:
            # Initialize the tokens dictionary
            self.tokens_info = {}

            # Do the lazy tokenization and save the results
            for doc_tokens in lazy_corpus_tokenization(documents):
                # Create the name of the file where the tokenization will be
                # saved
                doc_id = len(self.tokens_info) + 1
                doc_name = self.tokens_prefix + str(doc_id) + '.json'
                # Save the name in a dictionary for later use.
                self.tokens_info[doc_id] = doc_name
                # Save the tokenization in a file.
                self._save_document(doc_name, doc_tokens)

            # Save the index of the tokens.
            index_path = join(tokens_folder_path, self.tokenization_index_name)
            with open(index_path, 'w') as file:
                json.dump(self.tokens_info, file)

            # -- Find the Phrases in the documents and add them to their
            # tokenization --
            # First -> Train the Phrase Model with our corpus.
            phrase_model = Phrases(self.corpus_tokens())
            # Second -> Export the trained model to use less RAM, faster
            # processing (Model updates are no longer possible).
            phrase_model = phrase_model.freeze()
            # Last -> Add the Bigrams, Trigrams, etc... to each of the tokenized
            # documents.
            for file_name in self.tokens_info.values():
                # Load the list of tokens in the document.
                doc_tokens = self._load_document(file_name)

                # Apply the model to each document to find the phrases they have
                for token in phrase_model[doc_tokens]:
                    # Check if the current token is a 'phrase'
                    if '_' in token:
                        # Add the new phrase to the tokens of the document.
                        doc_tokens.append(token)

                # Save the changes made to the current tokenized document.
                self._save_document(file_name, doc_tokens)

    def corpus_tokens(self):
        """
        Load, one at a time, the saved tokenized Documents.
        :return: a sequence of the tokens of the documents in the corpus.
        """
        # Iterate through the names of the files where the tokens are stored
        for file_name in self.tokens_info.values():
            # Load each tokenized document and return it one at a time.
            doc_tokens = self._load_document(file_name)
            yield doc_tokens

    def _load_document(self, file_name):
        """
        Load a tokenized document with the given file name.
        :param file_name: The name of the file where the tokenized document is
        saved.
        :return: The Document saved in the file with the given name.
        """
        # The path of the folder for the tokenized documents.
        tokens_folder_path = join(self.data_folder, self.tokens_folder)
        # Create the full path of the file
        document_path = join(tokens_folder_path, file_name)

        # Load the tokens list of the document.
        with open(document_path, 'r') as file:
            doc_tokens = json.load(file)

        # Return the list of tokens
        return doc_tokens

    def _save_document(self, file_name, doc_tokens):
        """
        Save a tokenized document to a file with the given name.
        :param file_name: The name of the file where the tokenized document will
        be saved.
        :param doc_tokens: The tokenized document that will be saved to a file.
        """
        # The path of the folder for the tokenized documents.
        tokens_folder_path = join(self.data_folder, self.tokens_folder)
        # The path of the file where the document will be saved.
        file_path = join(tokens_folder_path, file_name)

        # Save the tokenized document.
        with open(file_path, 'w') as file:
            json.dump(doc_tokens, file)

    @classmethod
    def are_tokens_saved(cls):
        """
        Check if the tokens from a previos tokenizer are saved and ready to
        be used.
        :return: Bool representing if we have the tokens or the corpus saved or
        not.
        """
        # The path of the folder for the tokenized documents.
        tokens_folder_path = join(cls.data_folder, cls.tokens_folder)
        # Location of the index file
        index_path = join(tokens_folder_path, cls.tokenization_index_name)

        # Check if the index file exists.
        if not isfile(index_path):
            return False
        # Open the index file, and check there is information available.
        with open(index_path, 'r') as file:
            tokens_info = json.load(file)
        # Check if token_info has null values or is empty.
        if not tokens_info or not len(tokens_info) or not isdir(tokens_info):
            return False
        # The Tokenization Index is ready and available.
        return True

    @classmethod
    def saved_tokenizer(cls):
        """
        Creates a CorpusTokenizer from the information saved by a previous
        tokenizer.
        :return: A CorpusTokenizer
        """
        return cls(None, _use_saved=True)
