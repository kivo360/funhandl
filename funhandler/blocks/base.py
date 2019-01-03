from abc import ABC
import uuid
import threading
from multiprocessing import Queue as MQueue

class BaseBlock(ABC):
    """
        Blocks work a lot like agents inside for reinforcement learning.
        A block has the following:
            - step
                - The step function iterates through all of the proper states and modifies them according to a given action
            - 
    """
    def __init__(self, name, type_name, **kwargs):
        self.name = name
        self.type_name = type_name
        self.required = [] # Set a list of required types that need to be added
        self.current_id = str(uuid.uuid4())

    def __call__(self, **kwargs):
        """ Will get all of the requirements of each object and try setting unfilled requirements from the main state"""
        raise NotImplementedError

    def step(self, action, **kwargs):
        # Run the execute when the run function is run for the session. 
        raise NotImplementedError
    
    def check_required(self):
        """ Checks for required objects. Usually understood by checking types """
        raise NotImplementedError

    def add_requirements(self, *args):
        """ Checks for required objects. Usually understood by checking types """
        raise NotImplementedError
    
    def reset(self):
        # Run the execute when the run function is run for the session. 
        raise NotImplementedError

    

    def __repr__(self):
        capname = self.type_name.capitalize()
        return "<{0} 0x:{2} -- {1}>".format(capname, self.name, self.current_id)


class StateBlock(ABC):
    """
        This block is used to save and store states. The state is usually to store information about what the session will need
    """
    def __init__(self, name, type_name, **kwargs):
        self.name = name
        self.type_name = type_name
        self.required = [] # Set a list of required types that need to be added
        self.current_id = str(uuid.uuid4())

    def __call__(self, **kwargs):
        """ Will get all of the requirements of each object and try setting unfilled requirements from the main state"""
        raise NotImplementedError

    
    def check_required(self):
        """ Checks for required objects. Usually understood by checking types """
        raise NotImplementedError

    def add_requirements(self, *args):
        """ Checks for required objects. Usually understood by checking types """
        raise NotImplementedError
    
    def reset(self):
        # Run the execute when the run function is run for the session. 
        raise NotImplementedError

    def step(self, action, **kwargs):
        # Run the execute when the run function is run for the session. 
        raise NotImplementedError
    

    def __repr__(self):
        capname = self.type_name.capitalize()
        return "<{0} 0x:{2} -- {1}>".format(capname, self.name, self.current_id)


class ActionBlock(ABC):
    """
        This block is used to save and store states. The state is usually to store information about what the session will need
    """
    def __init__(self, name, type_name, **kwargs):
        self.name = name
        self.type_name = type_name
        self.required = [] # Set a list of required types that need to be added
        self.current_id = str(uuid.uuid4())

    def __call__(self, **kwargs):
        """ Will get all of the requirements of each object and try setting unfilled requirements from the main state"""
        raise NotImplementedError

    
    def check_required(self):
        """ Checks for required objects. Usually understood by checking types """
        raise NotImplementedError

    def add_requirements(self, *args):
        """ Checks for required objects. Usually understood by checking types """
        raise NotImplementedError
    


    def action_filter(self):
        raise NotImplementedError
    
    def reset(self):
        # Run the execute when the run function is run for the session. 
        raise NotImplementedError

    def step(self, action, **kwargs):
        # Run the execute when the run function is run for the session. 
        raise NotImplementedError
    

    def __repr__(self):
        capname = self.type_name.capitalize()
        return "<{0} 0x:{2} -- {1}>".format(capname, self.name, self.current_id)
    

"""
    Action Block:
    
    dispatch = DispatchOrder()
    dispatch.step(buy, trade="BTC", base="USDT", exchange="binance") # returns a general portfolio and dispatches to everything
"""
