""" 
Local file handling for media files.  Uses temp storage.
"""
import os
import os.path
from talkback.core import BackendException

file_dir = os.environ.get('TALKBACK_LOCALFILE_DIR',None)

def set_file(file_to_store):
    """ 
    Sets the file in local storage. Returns file name.
    """
    try:
        if not file_dir:
            raise BackendException('Must set TALKBACK_LOCALFILE_DIR to use locafile storage.')
    
        prefix, incoming_filename = os.path.split(file_to_store.name)
        with file(os.path.join(file_dir,incoming_filename),'wb') as storefile:
            while True:
                buf = file_to_store.read(1024)
                if buf:
                    storefile.write(buf)
                else:
                    break
            
            return incoming_filename
    finally:
        file_to_store.close()

def get_file(filename):
    """ 
    Gets the specified file from local storage.
    """
    if not file_dir:
        raise BackendException('Must set TALKBACK_LOCALFILE_DIR to use locafile storage.')
    
    return file(os.path.join(file_dir,filename),'rb')
