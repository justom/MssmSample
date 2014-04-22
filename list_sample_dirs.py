# Initial Problem description:

# I have a folder that contains a number of subdirectories.  Some, but not
# all, of the subdirectories follow a naming convention that consists of three
# elements, separated by underscores. These elements are:

# 1. a sample name (alphanumeric characters plus underscore)
# 2. a cycle number (the letter "C" followed by exactly three digits)
# 3. a date (exactly six digits)

# For example, the following names conform to this convention:

# - PT000_Normal_C002_130905
# - LA_C134_130902
# - 13006_C200_130912

# Write me a program that, given a directory, prints out all subdirectory names
# that follow the convention.  Furthermore, print out the word "MAX" followed by
# the subdirectory name that contains the highest cycle number.


# Additional info: 
# 1. Only search the top-most directory
# 2. Multiple instances of CXXX in filenames are acceptable; use the
#    final one as the cycle name if it's a valid strong.
# 3. Don't worry about validating the date as long as it's a valid number.

import logging
logging.basicConfig(level=logging.WARNING)

def list_sample_dirs(dir):
    '''Given a directory, list all subdirectories (depth 1) that contain samples.'''
    logging.warning("Unimplemented.")
    return False

def parse_cycle_number(str):
    '''Given a directory name find the cycle number of the sample, or return False if not a valid sample name.'''
    # A valid sample directory should have a prefix ([a-zA-Z0-9_]), a
    # cycle number, and a date, separated by underscores.
    logging.warning("Unimplemented.")
    return False

def is_valid_date(str):
    '''Valid dates are strings of six digits.'''
    # match \d{6}
    logging.warning("Unimplemented.")
    return False

def is_valid_cycle(str):
    '''A valid cycle string is of the form CXXX where X are digits.'''
    # match C\d{3}
    # make an assumption about 'c' vs 'C'
    logging.warning("Unimplemented.")
    return False

if __name__ == "__main__":
    list_sample_dirs(".")

