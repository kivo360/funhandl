# Cisco Environmental Challenge will Work

On the outside I understand I seem scattered. Between working on the Cisco Challenge, the trading bot, and the social networking service, it seems as though I'm not working effectively. However, this is not fully the case. As I was talking to somebody that explained exactly that idea (that I need focus), I decided to write down exactly my thoughts.

## Synergetic Processes

The cisco challenge will primarily be out trading bot. It will only be the trading bot realisically. However, the concept of balancing **multiple variables indirectly**. When handling accounts between different exchanges, we'll need to account for the bots that already exist, the correlated changes for when we buy/sell, as well as the random slipage that can happen.

In other words, running through larger scale is rough. It requires more than just predicting things. It requires balancing out variables that we normally don't think about. **It requires multiple agents to cooperate to prevent wiping out our user's funds. Representing every part of the process.**

Working on the Cisco project can give us 2 things. Which can open a world of possibilities:

1. Publicity
2. Money 
3. Outside mentorship to progress the project forward
    1. This could include new investors
    2. This could include new educational institutions
    3. This also can include other entreprenuers that can teach us what to do.


## Requirements to finish the reinforcement bot integration:

### Global session management

* This means creating a way to store what’s happening while trades are taking place, ways to monitor what’s happening with trades. (SARSA state management)
* A way to store models while running them live
* A way to dynamically place global items into the same place to be able to monitor them in a non-blocking way.
### Simulation - Used to check and prevent overfitting models. Also used to 
* So far we have stochastic sampling
* Creation of a deep markov chain model to replace that stochastic sampling
    * Should help with polyphasic sequencing inside of the the trading simulation. 
    * The pyro ai application works very well to explain this
    * Use Agent Based Modeling to create better than random examples

### Reinforcement System

Here we place the live learning system online. Just like the cart-pole system holds the pole suspending on the cart in a verticle manner, the reinforcement learning will be used to be able to balance forces inisde of supply lines. 

The objective is to create a reninforcement system to balance portfolios and prices between multiple bots compared to the outside system, and ensure something like self-organized criticality don't destroy profits by accident. 


https://medium.com/@tuzzer/cart-pole-balancing-with-q-learning-b54c6068d947


## Requirements to Win The Cisco Challenge

### Global session management

* Creating a storage system that exist between different agents
* A way to monitor pricing of various goods
* A way to step through an environment

### Simulation - Used to check and prevent overfitting models. Also used to.
* Create a deep markov chain that allows us to model various assets
* Agent-Based Modelling to create a general market for tokens and price of producing assets and services. The simulations will work to make sure we have multiple agencies doing various tasks with each other, and at the same time create a correlation with the pricing of various tokens. This way, we could model the valutaitons structures between various activities. Each one, affecting the others.
* Can use mesa to determine lag 

### Reinforcement System

Each reinforcement agent should have a series of actions (such as increasing access to liquidity, buying certain asset types, or backing certain types of assets over time). The agents made on the side will have simple ways of acting for the bots to respond to. Much like the orderbook or pries in an exchange.

The objective is to create a reninforcement system to balance portfolios and prices between multiple bots compared to the outside system, while also growing our desired outputs, and ensure something like self-organized criticality don't destroy outputs by accident. 


https://medium.com/@tuzzer/cart-pole-balancing-with-q-learning-b54c6068d947


As you can see, the two requirements are nearly the exact same. The only key difference is the data feed to the reinforcement algorithms. However, the data provided is relatively the same as well. 