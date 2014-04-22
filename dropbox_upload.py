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

import sys, logging
from dropbox import client, rest, session

def upload_file_to_dropbox(src, dest):
    '''Move the file specified in src to the destination specified on dropbox.'''
    logging.warning("upload_file_to_dropbox: Unimplemented.")
    return None

def parse_csv_file(filename):
    '''Given a csv file, parse it into a collection of pairs of source
    files and their destinations.  For bad entries in the CSV file,
    log a warning and continue, rather than aborting.'''
    logging.warning("parse_csv_file: Unimplemented.")
    return None

def main(csv_file):
    '''Parse the CSV file and then for each result attempt to upload the file to dropbox.'''
    print csv_file

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        logging.error("Usage: dropbox_upload path_to_csv_file")

