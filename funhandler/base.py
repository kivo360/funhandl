import sys
from funtime import Store, Converter
# this is a pointer to the module object instance itself.
this = sys.modules[__name__]
# Use these variables to handle the database
this.store_name = 'datahandler'
this.host = None
this.db = None


def set_host(host):
    if (this.host is None):
        # also in local function scope. no scope specifier like global is needed
        this.host = host
    else:
        msg = "Database is already initialized to {0}."
        form = msg.format(this.host)
        raise RuntimeError(form)

def set_lib_name(name):
    this.store_name = name

def initialize_database():
    """
        Globally set the database here
    """
    # TODO: Refactor the funtime library
    this.db = Store(this.host).create_lib(this.store_name).get_store()

    
    

# TODO: Set storage location eventually too for the parkquet file