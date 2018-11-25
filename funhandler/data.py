import sys
import time
import pandas as pd
from funpicker import Query, QueryTypes
# this is a pointer to the module object instance itself. 
# NOTE: We use this to set module-wide variables such as the storage location
this = sys.modules['funhandler']

# TODO: add proper logging

def add_bars(data):
    """ Adds the bars of the current data to the database

    This function receives list(dict) or will convert pd.DataFrame
    to list(dict). Data should contain required keys in it that
    will be used to query `funpicker`. Once funpicker response is
    ready data will be stored to `funtime`.

    Function will do basic validation on the incoming data.
    --------------------------------------------------------------

    Parameters
    ----------
    data: list(dict)
        List of lookups 
    Returns
    -------
    bool
        False - if anything went wrong TODO: add exceptions
        True - if bars were saved successfully

    Raises
    ------
    AttributeError
        Raised when passed datatype is not correct

    KeyError
        Raised when required keys missing in passed data
        
    """

    # Start validation of incoming  data

    # 0. If data is None, return False
    if not data:
        return False
    # 1. Check if datatype of incoming data is list(dict)
    #    If data is a pd.DataFrame -> convert it to list(dict)
    if not isinstance(data, list):
        if isinstance(data, pd.FataFrame):
            data = data.to_dict('records')
        else:
            raise AttributeError("Not valid datatype for param data provided."
                                 "Datatype has to be list(dict) or pandas.DataFrame.")

    # 2. Ensure all of the necessary keys are here
    required_keys = ['base', 'trade', 'exchange', 'period', 'timestamp', 'type']
    for item in data:
        keys = item.keys()
        if not set(required_keys).issubset(keys):
            raise KeyError("Some required keys are not present in dataset:"
                           f"dataset: {keys}, required: {required_keys}")

        # NOTE:
        # we can start processing and pulling data from funpicker at this
        # point. The question is: do we want to know if all dataset has valid
        # keys first or not?

        # The way I would think we need to do is to skip whatever lines are not correct and
        # process what we can and maybe record where data was wrong and retun 'Warnings' back
        # to user.

    # End validation

    # Get bars data from `funpicker`
    list_of_results = []
    for item in data:
        result = _get_bars_data_from_funpicker(**item)
        if (isinstance(result, dict)
            and result.get('Response')
            and result['Response'] == 'Error'):
            print(f"Error for a pair: {item['base']}-{item['trade']} | "
                  f"Message: {result.get('Message')}")
            continue
        if not result:
            continue
        # TODO: remove all NaN as 0
        save_to_funtime(result, **item)

    return True

def _get_bars_data_from_funpicker(data={},limit=30,**kwargs):
    crypto = kwargs['base']
    fiat = kwargs['trade']
    exchange = kwargs['exchange']
    period = kwargs['period']
    # query_type = kwargs['type']

    fpq = Query().set_crypto(crypto).set_fiat(fiat).set_exchange(exchange).set_period(period).set_limit(limit).get()
    return fpq

def save_to_funtime(data, **kwargs):
    """ Store data results to funtime

    Parameters
    ----------
    data: list(dict)
        Response data from funpicker
    """
    data_type = kwargs.get('type', 'price')
    timestamp = kwargs.get('timestamp', None)
    for item in data:
        # TODO: funtime doesn't have store_many functionality as of right now.
        # once that is added we should be able to pass a list to funtime and
        # it will handle batch load.
        item['type'] = data_type       
        item['timestamp'] = timestamp
        if timestamp:
            this.db[this.store_name].store(item)

def load_data(base, trade, exchange, limit=500, period='minute', latest=False, start=time.time()):
    # if data exist with the given parameters pull from the funtime library

    # Create a pandas dataframe for the data

    # Create a parquet file

    # Save the parquet file somewhere

    # Add the location into funtime
    return True


def get_latest_data(query_args):
    if not isinstance(query_args, dict):
        return False, {} 

    last_ran = list(this.db[this.store_name].query_latest({'limit': 1, **query_args}))
    if len(last_ran) == 0:
        # Find something to do here
        return False, {}
    
    return True, last_ran[0]



def get_latest_bar(base, trade, exchange, limit=500, period='minute', latest=False, start=time.time()):
    # Load the latest bars from the last loaded data (inside of the funtime library)

    # Turn parquet file into latest bar

    # If theres no ran_bars for the latest bars, create a new dataframe and save to funtime for record
    # If there is ran_bars, get the latest for the given type of information (see)
    
    # Query information goes here
    
    q_info = {'base':base, 'trade':trade, 'exchange': exchange, 'limit': limit, 'period': period, 'type': 'loaded_bars'}
    # Should have the latest table or nothing
    latest_bar_table = get_latest_data(q_info)

    if latest_bar_table[0] == False:
        raise AttributeError("Bar doesn't exist")

    # TODO: Pop the latest bar from this table. Ensure it's removed
    # This can be done using the tutorial available here:
        # https://stackoverflow.com/questions/39263411/pandas-pop-last-row
    

    # TODO: Save the new
    return True
