# Funhandler Developer Docs

Funhandler is the datahander for the live testing library. The overall idea behind this library is that the user will be able to enter new information for the backtest of the system.

It's meant to be the the modual version of the data handler inside of the backtesting tutorial: 

https://www.quantstart.com/articles/Event-Driven-Backtesting-with-Python-Part-III

The general idea works like the following:

1. The user is able to set the location of the database (a mongodb database)
2. The user sends a dataframe representing the data that they need to save.
3. The data is saved into the mongo database.
4. To backtest we load the data of a trade pair based on a given timeframe.
5. We can begin pulling the latest time for a given trade pair.
6. If we have no more bars loaded in the latest pair return false to indicate the cycle is finished.


## Desired Use Case
```python

# Import Funhander
import funhandler as fh

MONGOHOST = 'localhost'

fh.set_host(MONGOHOST)
fh.initialize_database()

# This is the data for a given time period
df = pandas_data

# Adds the trading bars into the system. (funtime)
fh.add_bars(df)

tf = twitter_dataframe
# Can add other kinds of information
fh.add_data('tweets', tf)


# Loads a series of bars into the file
fh.load_bars('BTC', 'USD', 'binance')

# This will return false if there are no more bars available
while fh.is_still_bars('BTC', 'USD', 'binance'):
    # Should have a dataframe to get the latest bar for the user to analyze
    barframe = fh.get_latest_bar('BTC', 'USD', 'binance') # Should be increasing as ths is_still_bars decreases
```

## Desired Inner Workings
Internally the inner workings should allow for scale. The reasoning is that we'd be able to run multiple backtest at the exact same time asyncronously. This will be so we can ensure our AI is well trained at scale. This means the following:

1. The added bars will have to exist inside of a database
2. The loaded bars will have to be stored somewhere for later access. We  recommend [parquet](https://github.com/dask/fastparquet) stored inside of a global store such as S3. The location of the saved file will be referrable inside of the funtime library.
    - This is so we can run through the effort of pulling the data at scale and with different sources at the same time.
    - With this design we could pull anything. 
3. We would want to placed the latest bar inside of a parquet file as well. It should append the latest bar into the composite column data and return the relavant information for the backtest.


## TODO Items

- [ ] Create a storage adapter
    - Here we make sure to be able to figure out how and where we want to stor the information. If an allocated folder doesn't exist we create it. Start with local storage.
- [ ] Store a file
    - Store a file and return the location for the file. It could be a local location or something like s3 or ipfs.
- [ ] Load a file
    - Load a parquet file. If it's in an s3 location, try pulling it and loading that file.
- [ ] Load a recent doc
    - Load a placeholder frame to pop a recent row
- [ ] Pop the most recent row inside of the placeholder session
    - Here we pull from the most recently sorted


## Questions you're probably asking

### 1. What is a placeholder?
The placeholder is a currently loaded segment of the bar data. It's used to be able to run backtest in a partially scalable way. It's basically a session between the source of data and what's analyzing the data. This is good to allow us to isolate what we're analyzing


POOL OF DATA ---> STORE SESSION IN FILE <---->  TEMPORARY CURRENTLY USED DATA --->  USE FOR ANALYTICS

### 2. Why Build A Module?
It's smart to build a module to separate dependencies. Keeping the code away from an archaic structure in runtime. The current codebase is archaic, and needs some separation to upgrade beyond its current stage. This datahandler module is going to be used to help us run backtest/stochastic test in scale.

### 3. How Long Do I Have To Figure This Out?
We'll discuss the amount of time. However, if you follow the coding guide inside of the tutorial available [here](https://www.quantstart.com/articles/Event-Driven-Backtesting-with-Python-Part-III). It's apart of a much larger event driven backtesting system. Please read the first two articles then run through all of the datahandler with sample list to understand what it is. Then start this project. If you do, the main work should take 2-3 days

### 4. What Will Happen With This Work?

Open source it. In the event that we finish this app we're both placing it into production and placing it into Funguana's Open Source. The data pipeline is being worked on seperately.


## What You're Getting

The original set of code you have will have some parts of the overall working module. It'll have the necessary setters and getters so you(The developer), can create the necessary functions very quickly. The store will be working and the means of collecting the information will be provided by the library `funpicker`. 

The code currently provided is a shell of what's required. In the event that there is confusion to what is required, the tutorial explains what needs to happen.


## How to Run

This requires `pipenv` to run. From there the funhandler should work.

```bash
    pipenv install -e .
```