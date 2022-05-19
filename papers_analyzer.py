# Gelin Eguinosa Rosique

import json
from os import mkdir
from os.path import join, isfile, isdir

from papers import Papers
from extra_funcs import progress_bar, big_number
from time_keeper import TimeKeeper


class PapersAnalyzer:
    """
    Scans the CORD-19 papers to organize them by certain characteristics and
    return subsets of the papers by these characteristics when required.
    """
    # Class Data Locations
    data_folder = 'project_data'
    small_papers_index = 'small_papers_index.json'
    medium_papers_index = 'medium_papers_index.json'
    big_papers_index = 'big_papers_index.json'

    def __init__(self, show_progress=False):
        # Get the CORD-19 papers.
        self.cord19_papers = Papers()
        
        # ...no need to check for the data folder, because Papers() will create
        # one if it doesn't exist.
        
        # Create the paths for the indexes of the new paper groups.
        small_papers_path = join(self.data_folder, self.small_papers_index)
        medium_papers_path = join(self.data_folder, self.medium_papers_index)
        big_papers_path = join(self.data_folder, self.big_papers_index)
        
        # Check if the indexes for the small, medium, big papers were already
        # created.
        if (isfile(small_papers_path) and isfile(medium_papers_path)
                and isfile(big_papers_path)):
            # Load the indexes.
            with open(small_papers_path, 'r') as file:
                self.small_papers = json.load(file)
            with open(medium_papers_path, 'r') as file:
                self.medium_papers = json.load(file)
            with open(big_papers_path, 'r') as file:
                self.big_papers = json.load(file)
            # Show progress if required.
            if show_progress:
                total = len(self.cord19_papers.papers_index)
                progress_bar(total, total)
        else:
            # Create the indexes.
            indexes = self._organize_papers(show_progress)
            # Get the Papers Indexes.
            self.small_papers = indexes[0]
            self.medium_papers = indexes[1]
            self.big_papers = indexes[2]
            # Save them to their files.
            with open(small_papers_path, 'w') as file:
                json.dump(self.small_papers, file)
            with open(medium_papers_path, 'w') as file:
                json.dump(self.medium_papers, file)
            with open(big_papers_path, 'w') as file:
                json.dump(self.big_papers, file)

    def _organize_papers(self, show_progress=False):
        """
        Scan the papers inside the CORD-19 database and creates 3 different
        indexes for them depending on their size:
        - Small: For papers containing one paragraph or less (0-300 characters).
        - Medium: For papers containing one page or less (301-3,000).
        - Big: For papers containing more than one page (3,001 or more).

        :return: A tuple containing 3 dictionaries with the small, medium, and
        big indexes.
        """
        # Create Papers Indexes
        small_papers = {}
        medium_papers = {}
        big_papers = {}

        # Variables to display the function's progress.
        total = len(self.cord19_papers.papers_index)
        count = 0

        # Iterate through the papers in the CORD-19 database.
        for paper_cord_uid in self.cord19_papers.papers_index:
            # Get the content of the paper.
            paper_content = self.cord19_papers.paper_full_text(paper_cord_uid)
            # Get the size of the paper.
            paper_size = len(paper_content)

            # Assign the paper to one of the indexes.
            paper_dict = {'cord_uid': paper_cord_uid, 'size': paper_size}
            if paper_size <= 300:
                small_papers[paper_cord_uid] = paper_dict
            elif paper_size <= 3_000:
                medium_papers[paper_cord_uid] = paper_dict
            else:
                big_papers[paper_cord_uid] = paper_dict

            # Show Progress if required.
            count += 1
            if show_progress:
                progress_bar(count, total)

        # Return the indexes.
        return small_papers, medium_papers, big_papers

    def big_papers_content(self, n=-1, show_progress=False):
        """
        Get the content of 'n' numbers of big papers in the CORD-19 database and
        return them in lazy form. If the value of 'n' is -1, then return the
        content of all the big papers available.
        *** Papers with more than 1,000,000 characters are going to be ignored,
        because of Spacy's models don't accept documents that large without
        modifying their models.

        :return: An iterator of strings.
        """
        # Find the number of papers we can return.
        if n < 0:
            big_total = len(self.big_papers)
        else: 
            big_total = min(n, len(self.big_papers))

        # To keep track of the iterations.
        count = 0
        # Iterate through the first 'number' of big papers and return their
        # content.
        for cord_uid in self.big_papers:
            # Check if we have returned all the requested papers.
            if big_total == count:
                break
            # Load new paper.
            paper_content = self.cord19_papers.paper_full_text(cord_uid)
            # Skip the text if it's too large for language processing.
            if len(paper_content) > 1_000_000:
                continue

            # Update counter and return the paper.
            count += 1
            yield paper_content

            # Show Progress if required.
            if show_progress:
                progress_bar(count, big_total)


def papers_analysis():
    """
    Analyze the CORD-19 papers, and classify them by the amount of characters
    they have.
    """
    # Get the papers and the amount available in the current database.
    the_papers = Papers()
    total = len(the_papers.papers_index)
    print(f"\nAmount of papers in CORD-19: {big_number(total)}.")

    # Counters for the different size of the papers.
    small = 0  # 0-300 characters (small paragraph)
    medium = 0  # 301-3,000 characters (less than a page)
    big = 0  # 3,001 - ... characters (bigger than a page)

    # Iteration variables.
    count = 0
    # Iterate through the papers contents to see how many of each size we have.
    print("\nAnalyzing the size of the papers...")
    for paper_content in the_papers.all_papers_full_text():
        # Update counter of papers viewed.
        count += 1
        # Print progress bar.
        progress_bar(count, total)

        # Check the size of the paper.
        if len(paper_content) < 301:
            small += 1
        elif len(paper_content) < 3_001:
            medium += 1
        else:
            big += 1
    
    print(f"\n\nPapers of one paragraph or less: {big_number(small)}.")
    print(f"\nPapers of one page or less: {big_number(medium)}.")
    print(f"\nPapers bigger than a page: {big_number(big)}.")


def biggest_papers():
    """
    Get how many papers are bigger than 1,000,000 characters.
    """
    # Get the papers and the amount available in the current database.
    the_papers = Papers()
    total = len(the_papers.papers_index)
    print(f"\nAmount of papers in CORD-19: {big_number(total)}.")

    # Iteration variables.
    biggest = 0
    count = 0
    # Iterate through the papers contents to see how many of each size we have.
    print("\nAnalyzing the size of the papers...")
    for paper_content in the_papers.all_papers_full_text():
        # Update counter of papers viewed.
        count += 1
        # Print progress bar.
        progress_bar(count, total)

        # Check the size of the paper.
        if len(paper_content) > 1_000_000:
            biggest += 1

    print(f"\n\nPapers with more than 1,000,000 characters: {big_number(biggest)}.\n")


# Test and check the sizes of the papers in CORD-19.
if __name__ == '__main__':
    # Record the Runtime of the Program
    stopwatch = TimeKeeper()

    print("\nAnalyzing the Paper sizes...")
    analyzer = PapersAnalyzer(show_progress=True)
    print("Done.")
    print(f"[{stopwatch.formatted_runtime()}]")

    small_count = len(analyzer.small_papers)
    medium_count = len(analyzer.medium_papers)
    big_count = len(analyzer.big_papers)
    total_count = small_count + medium_count + big_count
    print(f"\nThe total amount of Papers is: {big_number(total_count)}")
    print(f"The amount of Small Papers is: {big_number(small_count)}")
    print(f"The amount of Medium Papers is: {big_number(medium_count)}")
    print(f"The amount of Big Papers is: {big_number(big_count)}")

    print("\nExtracting the content of 5 Big Papers...")
    # Check if the testing_data folder exists.
    testing_folder = 'testing_data'
    if not isdir(testing_folder):
        mkdir(testing_folder)
    # Extract 5 papers.
    paper_count = 0
    for paper_text in analyzer.big_papers_content(5, show_progress=True):
        # Create Paper name.
        paper_count += 1
        paper_file = 'extracted_paper_' + str(paper_count) + '.txt'
        # Save the extracted paper.
        paper_path = join(testing_folder, paper_file)
        with open(paper_path, 'w') as f:
            print(paper_text, file=f)
    # Done with extracting the 5 Big Papers.
    print("Done.")
    print(f"[{stopwatch.formatted_runtime()}]\n")
