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


import sys, logging, os, cmd, re
import json
import locale
import pprint
import shlex
import dropbox
#from dropbox import client, rest, session

logging.basicConfig(level=logging.DEBUG)

# Hard code these for now
APP_KEY = 'leikm3a4vbv3h9n'
APP_SECRET = 'gbwce6od65g3f9g'
STATE_FILE = 'dropbox_upload.json'

def load_state():
    if not os.path.exists(STATE_FILE):
        return {}
    f = open(STATE_FILE, 'r')
    state = json.load(f)
    f.close()
    return state

def save_state(state):
    f = open(STATE_FILE, 'w')
    json.dump(state, f, indent=4)
    f.close()

def link_to_dropbox():
    state = load_state()
    uids = state.keys()
    client = None
    if len(uids) != 1:
        auth_flow = dropbox.client.DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)
        
        # Make the user log in and authorize this token
        url = auth_flow.start()
        sys.stdout.write("1. Go to: %s\n" % url)
        sys.stdout.write("2. Authorize this app.\n")
        sys.stdout.write("3. Enter the code below and press ENTER.\n")
        auth_code = raw_input().strip()

        access_token, user_id = auth_flow.finish(auth_code)
        client = dropbox.client.DropboxClient(access_token)
        account_info = client.account_info()

        sys.stdout.write("Link successful. %s is uid %s\n" % (account_info['display_name'], account_info['uid']))

        state = load_state()
        state[account_info['uid']] = {
        'access_token' : access_token,
        'display_name' : account_info['display_name'],
        }
        
        save_state(state)

    uid = uids[0]
    token = state[uid]['access_token']
    logging.debug("token created: " + uid + ":" + token)
    if client is None:
        client = dropbox.client.DropboxClient(token)
    return client

def upload_file_to_dropbox(client, src, dest):
    '''Move the file specified in src to the destination specified on dropbox.'''
    
    if client is None:
        logging.warning('called upload_file_to_dropbox with invalid client')
        return None
    if not os.path.exists(src):
        logging.warning('Upload file: ' + src + ': file does not exist.')
        return None

    from_file = open(os.path.expanduser(src), "rb")
    client.put_file('/' + dest, from_file)
    return True

def test_upload_file():
    client = link_to_dropbox()

    # test that the method fails with an invalid client
    assert not upload_file_to_dropbox(None, "q2_test_data/file1", "file")
    
    # test that trying to upload a non-existent file returns None
    assert not upload_file_to_dropbox(client, "q2_test_data/dne.csv", "files/file1.txt")

    # Ensure that the targets don't exist on dropbox before running the functions.
    logging.debug("Look to see if files exist")
    upload_dests = ["files/file1.txt","special_name.txt"]
    for f in upload_dests:
        filename = f.split('/')[-1]
        logging.debug( "looking for: " + filename)
        results = client.search("/", filename)
        assert len(results) == 0

    logging.debug("Now upload a test file to the destinations.")
    for f in upload_dests:
        assert upload_file_to_dropbox(client, "q2_test_data/file1", f)

    # Ensure that the files exist on dropbox, and clean up
    for f in upload_dests:
        filename = f.split('/')[-1]
        results = client.search("/", filename)
        assert len(results) == 1
        logging.debug(results)
        # having verified that the file exists, remove it, since this is the test program
        client.file_delete("/" + f)
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
    test_upload_file()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        logging.error("Usage: dropbox_upload path_to_csv_file")

