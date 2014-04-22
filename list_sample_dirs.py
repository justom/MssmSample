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

import logging, re
logging.basicConfig(level=logging.DEBUG)

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
    if len(str) != 4:
        return False
    # match C\d{3} or c\d{3}
    # Match case-insensitive to be slightly liberal in what we accept.
    if None == re.match('C\d{3}', str, re.I):
        return False

    return True

def test_is_valid_cycle():
    logging.info("Test is_valid_cycle()")
    bad_cycles = ["", "0", "00", "00x", "1234", "C1234", "Cabc", " c123"]
    for each in bad_cycles:
        logging.debug( "invalid cycle: " + each)
        assert not is_valid_cycle(each)
    good_cycles = ["C000", "C999", "C123", "c456"]
    for each in good_cycles:
        assert is_valid_cycle(each)

def test_is_valid_date():
    logging.info( "Test is_valid_date()")
    bad_dates = ["", "0", "00", "00x", "1234", "C1234", "Cabc", 123456, "12354"]
    for each in bad_dates:
        assert not is_valid_date(each)
    good_dates = ["140422", "010101", "999999"]
    for each in good_dates:
        assert is_valid_date(each)

def test_parse_cycle_number():
    logging.info( "Test parse_cycle_number")
    invalid_subdirs = ["", "foobar", "a miscellaneous string", "bad prefix_C234_000000", "C002_130905", "PT000_Normal_C002__130905", "LA_C00_130905", "LA_001_130905"]

    for each in invalid_subdirs:
        assert not parse_cycle_number(each)
        
    valid_subdirs = {"PT000_Normal_C002_130905":2, "LA_C134_130902":134, "13006_C200_130912":200}
    for each in valid_subdirs.iterkeys():
        assert valid_subdirs[each] == parse_cycle_number(each)

def test_list_sample_dirs():
    logging.info( "Test list_sample_dirs() on some expected directories that have no samples.")
    list_sample_dirs("/var")
    list_sample_dirs(".")
    logging.info( "Test on the directory structure provided for this project.  MAX should be next to 13006_C200_130912.")
    list_sample_dirs("q1_test_data")
    
if __name__ == "__main__":
    test_is_valid_cycle()
    test_is_valid_date()
    test_parse_cycle_number()
    test_list_sample_dirs()
    

