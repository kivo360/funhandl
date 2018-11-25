"""
    funhandl.tests.test_bars
    ~~~~~~~~~~~~~~~~~~~~~~~
    funhandl tests for funhandler.data
    
"""
import pytest
import time

test_price_data = [
    {
        "type": "price",
        "base": "BTC",
        "trade": "ETC",
        "exchange": "binance",
        "period": "minute",
        "timestamp": time.time(),
    },
    {
        "type": "price",
        "base": "USD",
        "trade": "ETC",
        "exchange": "binance",
        "period": "minute",
        "timestamp": time.time(),
    },
]

# contains non valid keys
test_fail_price_data = [
    {
        "type": "price",
        "base": "BTC",
        "trade": "ETC",
        "exchange": "binance",
        "period": "minute",
        "timestamp": time.time(),
    },
    {
        "base": "USD",
        "trades": "ETC",
        "exchange": "binance",
        "per": "minute",
        "timestamp": time.time(),
    },
]

@pytest.mark.skipif(True, reason="Not implemented. Requires fixtures.")
def test_add_bars(db, test_price_data):
    db.add_bars(test_price_data)
    pass

def test_add_bars_non_valid_data(db):
    # TODO: add test that raises if datatype of data is not valid
    pass

def test_add_bars_non_valid_keys(db, test_fail_price_data):
    # TODO: add test that raises if required keys are not present in add_bars
    pass
