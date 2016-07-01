""" 
Top level media tests.
"""
from talkback import media
import sys
sys.path += '..'
import pytest
import tempfile
import filecmp

@pytest.fixture
def setup():
    """ 
    Sets up localfile.
    """
    from talkback.media import localfile
    localfile.file_dir = tempfile.gettempdir()

def test_set_file():
    """ 
    Tests setting a file into localfile storage.
    """
    setup()
    with file('examples/telco/resources/cave.png','rb') as infile:
        stored_filename = media.set_file(infile)
        assert stored_filename == 'cave.png'

    
def test_get_file():
    """ 
    Tests retrieving file from localfile storage.
    """
    setup()
    with file('examples/telco/resources/cave.png','rb') as infile:
        stored_filename = media.set_file(infile)
        assert stored_filename == 'cave.png'
    
    retrieved_file = media.get_file('cave.png')
    assert filecmp.cmp(retrieved_file.name,'examples/telco/resources/cave.png')
