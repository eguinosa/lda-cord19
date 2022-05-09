# Gelin Eguinosa Rosique

import csv
import json
from os import mkdir
from os.path import join, isfile, isdir
from collections import defaultdict

# To test the class
from random import randint
from time_keeper import TimeKeeper


class Papers:
    """
    Scans the CORD-19 dataset to create an index of it, saving all the relevant
    information for later use.
    """
    # CORD-19 Data Location
    cord19_data_folder = 'cord19_data'
    current_dataset = '2020-05-31'
    metadata_file = 'metadata.csv'

    # Project Data Location
    project_data_folder = 'project_data'
    papers_index_file = 'papers_index.json'

    def __init__(self):
        """
        Load the metadata.csv to create the index of all the papers available in
        the current CORD-19 dataset and save all the information of interest.
        """
        # Create a data folder if it doesn't exist.
        if not isdir(self.project_data_folder):
            mkdir(self.project_data_folder)
        # Form the papers index path.
        papers_index_path = join(self.project_data_folder, self.papers_index_file)
        # Check if the papers' index exists or not.
        if isfile(papers_index_path):
            # Load the Papers' Index.
            with open(papers_index_path, 'r') as file:
                self.papers_index = json.load(file)
        else:         
            # Create the index of the papers.
            self.papers_index = self._create_papers_index()
            # Save the Papers' Index
            with open(papers_index_path, 'w') as file:
                json.dump(self.papers_index, file)

    def _create_papers_index(self):
        """
        Create an index of the papers available in the CORD-19 dataset specified
        in the data folders of the class.
        """
        # Create the metadata path
        metadata_path = join(self.cord19_data_folder, self.current_dataset, self.metadata_file)

        # Dictionary where the information of the papers will be saved.
        papers_index = defaultdict(dict)

        # Open the metadata file
        with open(metadata_path) as file:
            reader = csv.DictReader(file)
            # Go through the information of all the papers.
            for row in reader:
                # Get the fields of interest.
                cord_uid = row['cord_uid']
                title = row['title']
                abstract = row['abstract']
                publish_time = row['publish_time']
                authors = row['authors'].split('; ')
                pdf_json_files = row['pdf_json_files'].split('; ')
                pmc_json_files = row['pmc_json_files'].split('; ')

                # Save all the information of the current paper, or update it
                # if we have found this 'cord_uid' before. Also, check if the
                # are not empty.
                current_paper = papers_index[cord_uid]
                current_paper['cord_uid'] = cord_uid
                current_paper['title'] = title
                current_paper['abstract'] = abstract
                current_paper['publish_time'] = publish_time
                current_paper['authors'] = authors
                if pdf_json_files != ['']:
                    current_paper['pdf_json_files'] = pdf_json_files
                if pmc_json_files != ['']:
                    current_paper['pmc_json_files'] = pmc_json_files

        # Transform the papers' index from a 'defaultdict' to a normal dictionary.
        papers_index = dict(papers_index) 
        return papers_index

    def paper_title_abstract(self, cord_uid):
        """
        Find the title and abstract of the CORD-19 paper specified by the
        'cord_uid' identifier, and return them together as a string.
        :param cord_uid: The Unique Identifier of the CORD-19 paper.
        :return: A string containing the title and abstract of the paper.
        """
        # Get the dictionary with the info of the paper.
        paper_dict = self.papers_index[cord_uid]
        title_abstract = paper_dict['title'] + '\n\n' + paper_dict['abstract']
        return title_abstract

    def paper_content(self, cord_uid):
        """
        Find the text of the 'cord_uid' paper in either the 'pmc_json_files' or
        the 'pdf_json_files'.
        :param cord_uid: The Unique Identifier of the CORD-19 paper.
        :return: A string with the content of the paper, excluding the title and
        abstract.
        """
        # Get the dictionary with the info of the paper
        paper_dict = self.papers_index[cord_uid]
        # Get the paths for the documents of the paper
        doc_json_files = []
        if 'pmc_json_files' in paper_dict:
            doc_json_files += paper_dict['pmc_json_files']
        if 'pdf_json_files' in paper_dict:
            doc_json_files += paper_dict['pdf_json_files']

        # Where we are going to store the text of the paper.
        body_text = ''
        # Access the files and extract the text.
        for doc_json_file in doc_json_files:
            doc_json_path = join(self.cord19_data_folder, self.current_dataset, doc_json_file)
            with open(doc_json_path, 'r') as f_json:
                # Get the dictionary containing all the info of the document.
                full_text_dict = json.load(f_json)

                # Get all the sections in the body of the document.
                last_section = ''
                for paragraph_dict in full_text_dict['body_text']:
                    section_name = paragraph_dict['section']
                    paragraph_text = paragraph_dict['text']
                    # Check if we are still on the same section, or a new one.
                    if section_name == last_section:
                        body_text += paragraph_text + '\n\n'
                    else:
                        body_text += '<< ' + section_name + ' >>\n' + paragraph_text + '\n\n'
                    # Save the section name for the next iteration.
                    last_section = section_name

                # If we find text in one of the documents, break, to avoid
                # repeating content.
                if body_text:
                    break
        # Return the found content.
        return body_text

    def paper_full_text(self, cord_uid):
        """
        Get all the contents of the paper 'cord_uid', which includes the title,
        abstract and the body text.
        :param cord_uid: The Unique Identifier of the CORD-19 paper.
        :return: A string containing the title, abstract and body text of the
        paper.
        """
        full_text = self.paper_title_abstract(cord_uid) + '\n\n' + self.paper_content(cord_uid)
        return full_text

    def all_papers_title_abstract(self):
        """
        Create an iterator of strings containing the title and abstract of all
        the papers in the CORD-19 dataset.
        :return: An iterator of strings.
        """
        for cord_uid in self.papers_index:
            yield self.paper_title_abstract(cord_uid)

    def all_papers_content(self):
        """
        Create an iterator containing the body text for each of the papers in
        the CORD-19 dataset.
        :return: An iterator of strings.
        """
        for cord_uid in self.papers_index:
            yield self.paper_content(cord_uid)

    def all_papers_full_text(self):
        """
        Create an iterator containing the full text for each of the papers in
        the CORD-19 dataset.
        :return: An iterator of strings.
        """
        for cord_uid in self.papers_index:
            yield self.paper_full_text(cord_uid)


# Testing the Papers class
if __name__ == '__main__':
    # Record the Runtime of the Program
    stopwatch = TimeKeeper()

    # Load the CORD-19 Dataset
    print("Loading the CORD-19 Dataset...")
    cord19_papers = Papers()
    print("Done.")
    print(f"[{stopwatch.formatted_runtime()}]")

    # Get the amount of documents the dataset has.
    num_papers = len(cord19_papers.papers_index)
    print(f"\nThe current CORD-19 dataset has {num_papers} documents.")

    # Get the 'cord_uid' of one of the papers.
    cord19_uids = list(cord19_papers.papers_index.keys())
    rand_i = randint(0, num_papers - 1)
    rand_cord_uid = cord19_uids[rand_i]

    # # Getting the embedding of one of the papers.
    # print(f"\nGetting the Embedding for the Paper <{rand_cord_uid}>...")
    # result = cord19_papers.paper_embedding(rand_cord_uid)
    # print(f"The Embedding is:")
    # print(result)

    # # Getting the title & abstract of one of the papers.
    # print(f"\nGetting the Title & Abstract of the Paper <{rand_cord_uid}>...")
    # result = cord19_papers.paper_title_abstract(rand_cord_uid)
    # print("Title & Abstract:\n")
    # print(result)

    # # Getting the text of one of the papers.
    # print(f"\nGetting the content of the Paper <{rand_cord_uid}>...")
    # result = cord19_papers.paper_content(rand_cord_uid)
    # filename = 'output.txt'
    # print(f"The content was printed to '{filename}'.")
    # with open(filename, 'w') as f:
    #     print(result, file=f)

    # Getting the full text of one of the papers.
    print(f"\nGetting the full text of the Paper <{rand_cord_uid}>...")
    result = cord19_papers.paper_full_text(rand_cord_uid)
    filename = 'output.txt'
    print(f"The full text was printed to '{filename}'.")
    with open(filename, 'w') as f:
        print(result, file=f)

    print("\nDone.")
    print(f"[{stopwatch.formatted_runtime()}]")
