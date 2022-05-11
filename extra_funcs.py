# Gelin Eguinosa Rosique


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
