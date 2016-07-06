""" 
Media backend that uses AWS S3 to store files.
"""
import os
from talkback.core import BackendException
import boto
from StringIO import StringIO

access_key_id = os.environ.get('AWS_ACCESS_KEY_ID',None)
secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY',None)
s3_bucket = os.environ.get('S3_BUCKET',None)

def _check_config():
    """ 
    Ensure config is ready.
    """
    if not (access_key_id and secret_access_key and s3_bucket):
        raise BackendException('Must define AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY and S3_BUCKET environment variables.')

def _bucket():
    """ 
    Gets the S3 bucket.
    """
    conn = boto.connect_s3()
    return conn.create_bucket(s3_bucket)

def set_file(file_to_store):
    """ 
    Sets the file in an S3 bucket. Returns URL.
    """
    _check_config()
    bucket = _bucket()
    key = boto.s3.key.Key(bucket)
    key.key = file_to_store.name
    key.send_file(file_to_store)
    return key.generate_url(3600)

def get_file(filename):
    """ 
    Gets the file from storage.
    """
    _check_config()
    bucket = _bucket()
    key = bucket.get_key(filename)
    outfile = StringIO()
    key.get_file(outfiile)
    return outfile
