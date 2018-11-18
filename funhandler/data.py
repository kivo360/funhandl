import sys
import time
import pandas as pd
# this is a pointer to the module object instance itself. 
# NOTE: We use this to set module-wide variables such as the storage location
this = sys.modules[__name__]

def add_bars(source, base, trade, exchange):
    """
        # ADD BARS
        ---

        Adds the bars of the current data source to the database.
    """

    # Some initial filtering here
    if not isinstance(source, pd.DataFrame):
        return False
    
    if not isinstance(base, str):
        return False
    
    if not isinstance(trade, str):
        return False
    

    # Ensure all of the necessary columns are here
    cols = source.columns
    
    # Ask me which data needs to be validated against
    if not set(['base','trade', 'exchange', 'period', 'timestamp']).issubset(cols):
        return False

    # Resample the data you insert here to the given time period

    # remove all nan as 0
    # Store data into the database here
    records = source.to_dict('records')

    # Store many into the funtime library
    this.db[this.store_name]
    return True




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