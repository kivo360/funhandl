import sys
import time
import pandas as pd
# this is a pointer to the module object instance itself.
this = sys.modules[__name__]
this.current_storage_type = ''
this.storage_information = {}

__AVAILABLE_TYPES__ = ['local', 's3']

def set_storage_model(model_type, **model_info):
    if not isinstance(model_type, str):
        return False
    
    if model_type not in __AVAILABLE_TYPES__:
        return False

def set_local_storage_info(**kwargs):
    # Should set a folder inside of the system
    # Should set a base path
    # Should set a folder to store the information inside of it.
    pass

def set_s3_storage_info(**kwargs):
    # Should ensure to set the AMI key
    # Should ensure to set the AMI secret
    # Should set the bucket
    # Should check to see if we have access to write to the bucket
    pass

def store_local_storage(file):
    """ Stores the file locally with the desired storage information """
    pass

def store_s3_storage(file):
    """ Stores the file inside of an s3 bucket """
    
    
    pass

def store_file(file):
    """ Should store the file inside of the allocated location. Default will be localhost """
    pass