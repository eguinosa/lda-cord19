# Gelin Eguinosa Rosique

# Use this code with a Jupyter Notebook, it won't work with the Python Console
# or Interpreter.

import logging
logging.captureWarnings(True)

import pyLDAvis
from pyLDAvis import gensim_models
from gensim import corpora
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from os.path import join


# Data Locations:
data_folder = 'project_data'
dict_file = 'dictionary.dict'
corpus_file = 'corpus_bow.mm'
current_lda_file = 'current_lda_model'

# Loading the dictionary, corpus and lda_model.
dict_path = join(data_folder, dict_file)
corpus_path = join(data_folder, corpus_file)
current_lda_path = join(data_folder, current_lda_file)
dictionary = Dictionary.load(dict_path)
corpus_bow = corpora.MmCorpus(corpus_path)
lda_model = LdaModel.load(current_lda_path)

# Use PyLDAvis to vizualize the topics
visual_data = gensim_models.prepare(topic_model=lda_model, corpus=corpus_bow, dictionary=dictionary)
pyLDAvis.enable_notebook()
pyLDAvis.display(visual_data)
