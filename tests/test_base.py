"""
    funhandl.tests.test_data
    ~~~~~~~~~~~~~~~~~~~~~~~
    funhandl tests for funhandler.base
"""

def test_init_db(db):
    db_data = db.get_db_params()
    assert db_data['host'] == 'localhost'
    assert db_data['store_name'] == 'test_store_name'
