#!/usr/bin/env python

# I have a file called ``files.csv``, which contains a list of files I want
# uploaded to Dropbox.  Each line contains a comma-separated pair of values: the
# first is the path of a file on your local machine, and the second is the path
# where we want the file to reside in a Dropbox folder.

# Write a command-line program that takes in one argument, the path to
# ``files.csv``, and then performs the uploads using the Dropbox API.

# Because of the way the Dropbox API is structured, you may find you need to ask
# for interactive input to perform user authentication.  This is absolutely fine;
# don't kill yourself delving into the underlying OAuth API.

# For testing purposes, we have a Dropbox folder set up called PBGCodingTest,
# with the following credentials::

#     App key: leikm3a4vbv3h9n
#     App secret: gbwce6od65g3f9g

# Don't feel like you have to use it; it is okay to just roll your own testing
# environment.  However, please provide some mechanism to allow us to run your
# code using the credentials above, be it via a command-line option, a config
# file, or some other method.

# Hard code these for now
APP_KEY = 'leikm3a4vbv3h9n'
APP_SECRET = 'gbwce6od65g3f9g'

import sys, logging, os
from dropbox import client, rest, session

logging.basicConfig(level=logging.DEBUG)

def upload_file_to_dropbox(src, dest):
    '''Move the file specified in src to the destination specified on dropbox.'''
    logging.warning("upload_file_to_dropbox: Unimplemented.")
    return None

def test_upload_file():
    assert not upload_file_to_dropbox("q2_test_data/dne.csv", "files/file1.txt")
    # XXX - assert that the files don't exist on dropbox before running the functions.
    assert upload_file_to_dropbox("q2_test_data/file1", "files/file1.txt")
    assert upload_file_to_dropbox("q2_test_data/file2", "special_name.txt")
    # XXX - assert that the files now exist on dropbox
    # XXX - remove the files from dropbox
    return

def parse_csv_file(filename):
    '''Given a csv file, parse it into a collection of pairs of source
    files and their destinations.  For bad entries in the CSV file,
    log a warning and continue, rather than aborting.'''
    results = []
    if not os.path.exists(filename):
        logging.warning(filename + ': file does not exist.')
        return results
    if not os.path.isfile(filename):
        logging.warning(filename + ': not a file.')
        return results

    csv_file = open(os.path.expanduser(filename), "r")
    for line in csv_file:
        components = line.strip().split(',')
        if len(components) != 2:
            logging.warning('Invalid line, skipping: ' + line)
        else:
            results.append([components[0],components[1]])
            logging.debug('Valid: ' + components[0] + ',' + components[1])
        
    return results

def test_parse_csv():
    directory_name = "q2_test_data"
    nonexistent_file = "q2_test_data/dne.csv"
    empty_file = "q2_test_data/empty.csv"
    invalid_file = "q2_test_data/invalid.txt"
    mixed_file = "q2_test_data/mixed.csv"
    good_file = "q2_test_data/files.csv"

    result = parse_csv_file('')
    assert len(result) == 0
    result = parse_csv_file(nonexistent_file)
    assert len(result) == 0
    result = parse_csv_file(directory_name)
    assert len(result) == 0
    result = parse_csv_file(empty_file)
    assert len(result) == 0
    result = parse_csv_file(invalid_file)
    assert len(result) == 0

    # the parse function should only ensure that the file format is
    # valid, not whether the contents specify files that exist.  The
    # uploading function will validate that the files exist before
    # processing them.
    result = parse_csv_file(mixed_file)
    assert len(result) == 5
    assert result[0] == ['./q2_test_data/file1', 'files/file1.txt']
    assert result[1] == ['./dne.csv', 'files/file1.txt']
    assert result[2] == ['./q2_test_data/file2','special_name.txt']
    assert result[3] == ['miscellaneous text','files/file1.txt']
    assert result[4] == ['./q2_test_data/file2','another_place.txt']

    result = parse_csv_file(good_file)
    assert len(result) == 2
    assert result[0] == ['./q2_test_data/file1', 'files/file1.txt']
    assert result[1] == ['./q2_test_data/file2','special_name.txt']

def main(csv_file):
    '''Parse the CSV file and then for each result attempt to upload the file to dropbox.'''
    test_parse_csv()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        logging.error("Usage: dropbox_upload path_to_csv_file")

