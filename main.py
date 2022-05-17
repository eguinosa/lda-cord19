# Gelin Eguinosa Rosique

from sys import argv
from pprint import pprint

from papers_analyzer import PapersAnalyzer
from corpus_tokenizer import CorpusTokenizer
from topic_processing import TopicManager
from time_keeper import TimeKeeper
from extra_funcs import big_number


if __name__ == '__main__':
    # To record the runtime of the program
    stopwatch = TimeKeeper()

    # Separate the CORD-19 papers by their size in 3 categories
    # (small - 1 paragraph, medium - 1 page, big - more than 1 page)
    print("\nSorting and separating the CORD-19 papers by size in 3 categories...")
    sorted_papers = PapersAnalyzer()
    print("Done.")
    print(f"[{stopwatch.formatted_runtime()}]")

    # Reporting the amount of Papers available by category.
    small_count = len(sorted_papers.small_papers)
    medium_count = len(sorted_papers.medium_papers)
    big_count = len(sorted_papers.big_papers)
    total_count = small_count + medium_count + big_count
    print(f"\nThe total amount of Papers in the CORD-19 is: {big_number(total_count)}")
    print(f"The amount of Small Papers is: {big_number(small_count)}")
    print(f"The amount of Medium Papers is: {big_number(medium_count)}")
    print(f"The amount of Big Papers is: {big_number(big_count)}")

    # Get the 30,000 documents from the 'big' category.
    print("\nExtracting 30,000 Big Papers from CORD-19...")
    papers_text = sorted_papers.big_papers_content(30_000)
    print("Done.")
    print(f"[{stopwatch.formatted_runtime()}]")

    # Tokenize the Documents:.
    print("\nTokenizing the documents...")
    # Load the CorpusTokenizer, if it was saved.
    if CorpusTokenizer.are_tokens_saved():
        print("Loading the saved tokenized documents.")
        tokenizer = CorpusTokenizer.saved_tokenizer()
    # Create the corpus tokenizer, if it can't be loaded.
    else:
        print("Tokenizing the documents from scratch.")
        tokenizer = CorpusTokenizer(papers_text)
    print("Done. ")
    print(f"[{stopwatch.formatted_runtime()}]")

    # Creating the Dictionary and the Corpus Bag-of-Words
    print("\nCreating the Dictionary and the Corpus Bag-of-Words...")
    # Load the Topic Manager if available, create it otherwise.
    if TopicManager.is_topic_manager_saved():
        print("Loading the saved dictionary and corpus bag-of-words.")
        topic_manager = TopicManager.saved_topic_manager()
    else:
        print("Creating the dictionary and corpus bag-of-words from scratch.")
        topic_manager = TopicManager(tokenizer)
    print("Done. ")
    print(f"[{stopwatch.formatted_runtime()}]")

    # Print Corpus Bag-of-Words Information
    print(f"\nNumber of unique tokens: {len(topic_manager.dictionary)}")

    # Train the LDA Model & Set training parameters.
    num_topics = 20
    chunksize = 20
    passes = 10
    iterations = 400
    eval_every = None
    # Check if the desired number of topics was passed as an argument in the
    # Command Line
    if len(argv) > 1:
        # We received a parameter from the command line.
        # Assume it is the desired number of topics.
        num_topics = int(argv[1])

    # Create and train the LDA Model
    print(f"\nTraining the LDA Model with {num_topics} topics...")
    lda_model = topic_manager.lda_model(num_topics,
                                        chunksize,
                                        passes,
                                        iterations,
                                        eval_every)
    print("Done. ")
    print(f"[{stopwatch.formatted_runtime()}]")

    # Printing Topics
    top_topics = lda_model.top_topics(topic_manager.corpus_bow)
    # Top Topics
    print("\nThe Top Topics are:")
    pprint(top_topics)

    # Average topic coherence
    average_coherence = sum([topic[1] for topic in top_topics]) / len(top_topics)
    print(f"\nThe {num_topics} topics average topic coherence is: {average_coherence:.4f}")

    # Print the total runtime of the program
    print("\nProgram Finished.")
    print(f"[{stopwatch.formatted_runtime()}]")
