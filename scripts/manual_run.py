import funhandler as fh
import time


def main():
    fh.set_host('localhost')
    fh.set_store_name('test_store_name')
    fh.set_storage_model('local')
    fh.set_local_storage_info(base_path='/tmp', storage_folder='parquet_data')
    fh.initialize_database()
    unique_data = {
        "type": "price",
        "base": "ETC",
        "trade": "BTC",
        "exchange": "binance",
        "period": "minute",
        "timestamp": time.time(),
    }
    fh.add_bars([unique_data])
    fh.load_data(**unique_data)

    while fh.is_still_bars(**unique_data):
        unique_data.update({'limit': 5})
        bars = fh.get_latest_bar_v2(**unique_data)
        print(bars)
    # call funpicker
    # from funpicker import Query, QueryTypes
    # fpq = Query().set_crypto('ETC').set_fiat('BTC').set_exchange('binance').set_period('hour').set_limit(30).get(QueryTypes['price'])

if __name__ == '__main__':
    main()
