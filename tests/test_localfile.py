""" 
Tests for localfile storage.
"""
import sys
sys.path += '..'
from talkback.media import localfile
import os
import tempfile
import pytest
import filecmp

@pytest.fixture
def setup():
    """ 
    Sets the directory.
    """
    localfile.file_dir = tempfile.gettempdir()

def test_set_file():
    """ 
    Tests setting a file into localfile storage.
    """
    setup()
    with file('examples/telco/resources/cave.png','rb') as infile:
        stored_filename = localfile.set_file(infile)
        assert stored_filename == 'cave.png'

    
def test_get_file():
    """ 
    Tests retrieving file from localfile storage.
    """
    setup()
    with file('examples/telco/resources/cave.png','rb') as infile:
        stored_filename = localfile.set_file(infile)
        assert stored_filename == 'cave.png'
    
    retrieved_file = localfile.get_file('cave.png')
    assert filecmp.cmp(retrieved_file.name,'examples/telco/resources/cave.png')
