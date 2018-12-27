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



def setup_funhandler():
    fh.set_host('localhost')
    fh.set_store_name('test_store_name')
    fh.set_storage_model('local')
    fh.set_local_storage_info(base_path='/tmp', storage_folder='parquet_data')
    fh.initialize_database()

def load_bars(bars):
    setup_funhandler()
    fh.add_bars([bars])
    fh.load_data(**bars)
    return bars

def process_bars(bars):
    setup_funhandler()
    while fh.is_still_bars(**bars):
        barframe = fh.get_latest_bar_v2(**bars)
        print(barframe) # this is where bar analysis can go

async def execute():
    unique_data = [
        {
            "type": "price",
            "base": "ETC",
            "trade": "BTC",
            "exchange": "binance",
            "period": "minute",
            "timestamp": time_1,
        }
    ]
    client = await Client(processes=True, asynchronous=True)
    source = Stream(asynchronous=True)
    (source.scatter()
           .map(load_bars)
           .rate_limit('500ms')
           .gather()
           .sink(process_bars))

    for data in unique_data:
        await source.emit(data)


if __name__ == '__main__':
    # timeout = 30 # timeout for 1 run
    # setup_funhandler()
    IOLoop().run_sync(execute)
    # client = Client()
