# Gelin Eguinosa Rosique

from sys import stdout

from papers import Papers

class PapersAnalyzer:
    """
    Scans the CORD-19 papers to organize them by certain characteristics and
    and return subsets of the papers by these characteristics when required.
    """
    # Class Data Locations
    project_data_folder = 'project_data'
    small_papers_index = 'small_papers_index.json'
    medium_papers_index = 'medium_papers_index.json'
    big_papers_index = 'big_papers_index'

    def __init__(self):
        # Get the CORD-19 papers.
        self.cord19_papers = Papers()
        
    #     # ...no need to check for the data folder, because Papers() will create
    #     # one if it doesn't exist.
        
    #     # Check if the indexes for the small, medium, big papers were already
    #     # created.
    #     small_papers_path = 

    # def _organize_papers(self):
    #     """
    #     Scan the papers inside the CORD-19 database and creates 3 different
    #     indexes for them depending on their size:
    #     - Small: For papers containing one paragraph or less.
    #     - Medium: For papers containing one page or less.
    #     - Big: For papers containing more than one page.
    #     """


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
    step_progress = total // 40
    # Iterate through the papers contents to see how many of each size we have.
    print("\nAnalyzing the size of the papers...")
    for paper_content in the_papers.all_papers_full_text():
        # Update counter of papers viewed.
        count += 1
        
        # Print progress bar.
        progress = count // step_progress
        percentage = count * 100 // total
        stdout.write('\r')
        stdout.write("[%-40s] %03s%%" % ('=' * progress, percentage))
        stdout.flush()

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


def big_number(number):
    """
    Add commas to number with more than 3 digits, so they are more easily read.
    """
    # Get the string of the number.
    number_string = str(number)
    
    # Return its string if it's not big enough.
    if len(number_string) <= 3:
        return number_string
    
    # Add the commas.
    new_string = number_string[-3:]
    number_string = number_string[:-3]
    while len(number_string) > 0:
        new_string = number_string[-3:] + ',' + new_string
        number_string = number_string[:-3]

    # Return the reformatted string of the number.
    return new_string


# Test and check the sizes of the papers in CORD-19.
if __name__ == '__main__':
    papers_analysis()
    
    # print(big_number(123_456_789))
    # print(big_number(23_456_789))
    # print(big_number(3_456_789))
    # print(big_number(89))

