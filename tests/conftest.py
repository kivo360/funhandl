"""
    funhandl.tests.conftest
    ~~~~~~~~~~~~~~~~~~~~~~~
    funhandl tests configuration and common fixtures
    
"""
import pytest

import funhandler as fh


@pytest.fixture
def db():
    fh.set_host('localhost')
    fh.set_store_name('test_store_name')
    fh.initialize_database()
    return fh
