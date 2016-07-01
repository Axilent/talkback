""" 
Media handling for Talkback.
"""
import os
from talkback.utils import get_module

def _backend():
    """ 
    Lazy initializes and retrieves the backend.
    """
    return get_module(os.environ.get('TALKBACK_MEDIA_BACKEND','talkback.media.localfile'))

def set_file(file_to_store):
    """ 
    Sets the file in the media backend.
    """
    return _backend().set_file(file_to_store)

def get_file(filename):
    """ 
    Gets the file from the media backend.
    """
    return _backend().get_file(filename)
