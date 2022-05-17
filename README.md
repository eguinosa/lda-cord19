# Using LDA on CORD-19

Running the Latent Dirichlet Allocation algorithm on the CORD-19 database, to find the topics presents in papers researching COVID-19.

## Introducción

En este proyecto trabajamos con 30,000 documentos de la base de datos CORD-19. Para garantizar que los documentos con los que trabajamos tienen una cantidad de contenido significativa, los papers del CORD-19 fueron separados en 3 categorías con respecto a su tamaño. Una categoría contiene los papers que contienen un párrafo o menos (0-300 caracteres), otra los que tienen una página (301-3,000 caracteres) o menos y la última categoría para los documentos con mas de una página (3,001 caracteres o más). De esta tercera categoría fue que extraimos los 30,000 documentos.

Después de extraer los 30,000 documentos del CORD-19, a estos le realizamos el proceso de tokenización donde eliminamos todas las stop-words, los simbolos de puntuación, números, luego de este proceso las palabras que quedan son llevadas a su ración utilizando lemmatización.

Con los 30,000 ya tokenizados, utilizamos el modelo LDA contenido dentro de la librería gensim para obtener tópicos presentes dentro de estos documentos, siempre brindando nosotros la cantidad de tópicos deseada.


## Clases y Metodos utilizados

__papers.py:__
Contiene la clase Papers() encargada de organizar los documentos del CORD-19, guardar toda la información relacionada con los papers, y extraer el contenido de los papers cuando sea necesario.

__papers_analyzer.py:__
Contiene la clase Papers_Analizer() que separa los papers del CORD-19 por su tamaño, y nos entrega la cantidad de documentos grandes (1 página o más) que deseemos, en este caso 30,000.

__corpus_tokenizer:__
Contiene la clase CorpusTokenizer(), encargada de procesar y tokenizar los textos de los papers, eliminando las palabras de poco interés (como las Stop-words), y luego del proceso de filtracion de palabras, lemmatizar los tokens que quedan.

__topics_processing.py:__
Contiene la clase TopicManager(), encargada de contruir el diccionario del corpus, la representación en bag-of-words de cada uno de los 30,000 documentos y el modelo LDA.

__main.py:__
Contiene la interface con la que interactúa el usuario, y donde se indica la cantidad de tópicos que se desea encontrar.


## Resultados

De los 138,967 documentos contenidos dentro del CORD-19, 21,824 son documentos pequeños de menos de un párrafo, 55,579 contienen solo una página y 61,564 más de una página.

##### LDA con 10 tópicos (topic coherence: -0.9758)

##### LDA con 15 tópicos (topic coherence: -0.9769)

##### LDA con 20 tópicos (topic coherence: -1.4661)

##### LDA con 40 tópicos (topic coherence: -3.7427)
