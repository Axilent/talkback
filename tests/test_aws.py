""" 
Tests for AWS S3 media backend.
"""
import sys
sys.path += '..'
from talkback.media import aws
import filecmp
import pytest
