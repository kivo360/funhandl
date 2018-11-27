import asyncio
from dask.distributed import Client
from streamz import Stream
from tornado.ioloop import IOLoop
from tornado import gen
import funhandler as fh
import time


time_1 = time.time()
time.sleep(2)
time_2 = time.time()

unique_data = [
    {
        "type": "price",
        "base": "ETC",
        "trade": "BTC",
        "exchange": "binance",
        "period": "minute",
        "timestamp": time_1,
    },
    {
        "type": "price",
        "base": "ETH",
        "trade": "BTC",
        "exchange": "binance",
        "period": "minute",
        "timestamp": time_2,
    },
]

def setup_funhandler():
    fh.set_host('localhost')
    fh.set_store_name('test_store_name')
    fh.set_storage_model('local')
    fh.set_local_storage_info(base_path='/tmp', storage_folder='parquet_data')
    fh.initialize_database()

    # fh.add_bars(unique_data)
    # fh.load_data(**unique_data)

def execute(data):
    fh.add_bars([data])
    fh.load_data(**data)

    while fh.is_still_bars(**data):
        barframe = fh.get_latest_bar_v2(**data)
        print(barframe)


if __name__ == '__main__':
    timeout = 10 # timeout for the set_bars() + get_bars()
    setup_funhandler()
    for item in unique_data:
        execute(item)
