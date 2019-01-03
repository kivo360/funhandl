from abc import ABC
import uuid
import threading
from loguru import logger
from multiprocessing import Queue as MQueue
from funhandler.state import MainState
from funhandler.blocks import BaseBlock, StateBlock

class Portfolio(BaseBlock):
    def __init__(self, name, **kwargs):
        super().__init__(name, "portfolio")
        
        self.required = []
        self.task_parts = {}
        self.dsk = None
        self.check_required(kwargs)
        # Loads the model.
       
        # portfolio is a portfolio manager object. Used to scale pushing information between various portfolios
        # a dispatch is something like a print or push to an outside location
        # Define a task graph here
    
    def load_tasks(self):
        logger.info("Portfolio Block")
    #      self.dsk = {'load': (self.task_parts['modloader'].load), # Loads a model based on the name (agent)
    #    'portfolio': (self.task_parts['portfolio'].load), # Loads a portfolio
    #    'environment': (self.task_parts['environment'].load), # Loads a portfolio
    #    'set': (self.set_env, 'load', 'portfolio', 'environment'), # create an object to step through
    #    'step': (self.step, 'set'), # Gets the next_state, reward and determination if the process is done
    #    'save-action-value': (self.task_parts['store'], 'step')}
    
    def check_required(self, kwds):
        kwkeys = kwds.keys()

        for i in self.required:
            if i not in kwkeys:
                raise AttributeError("{} not found in {}".format(i, self.__repr__()))

    def add_requirements(self, *args):
        for req in args:
            if isinstance(req, BaseBlock):
                self.task_parts[req.type_name] = req

    def set_env(self):
        pass

    def step(self, action, **kwargs):

        # Run the execute when the run function is run for the session. 
        print("Steping through the next")
    
    def reset(self):
        logger.debug("Reinforcement started")

class SARSALearning(BaseBlock):
    def __init__(self, name, **kwargs):
        super().__init__(name, "reinforcement")
        
        self.required = ["modloader", "portfolio", "environment", "dispatch", "modstore"]
        self.task_parts = {}
        self.dsk = None
        self.check_required(kwargs)

    
    def load_tasks(self):
        logger.success("Task loaded")
    #      self.dsk = {'load': (self.task_parts['modloader'].load), # Loads a model based on the name (agent)
    #    'portfolio': (self.task_parts['portfolio'].load), # Loads a portfolio
    #    'environment': (self.task_parts['environment'].load), # Loads a portfolio
    #    'set': (self.set_env, 'load', 'portfolio', 'environment'), # create an object to step through
    #    'step': (self.step, 'set'), # Gets the next_state, reward and determination if the process is done
    #    'save-action-value': (self.task_parts['store'], 'step')}
    
    def check_required(self, kwds):
        kwkeys = kwds.keys()

        for i in self.required:
            if i not in kwkeys:
                raise AttributeError("{} not found in {}".format(i, self.__repr__()))

    def add_requirements(self, *args):
        for req in args:
            if isinstance(req, BaseBlock):
                self.task_parts[req.type_name] = req

    def set_env(self, load, portfolio, environment):
        pass

    def step(self, **kwargs):
        # Run the execute when the run function is run for the session. 
        print("Steping through the next")
    
    def reset(self):
        logger.info("Porfolio Added")

class Session(object):
    def __init__(self, name, **kwargs):
        """
            raystate: boolean
                - determines if the shared state is a ray actor. 
                - If it's true we set send calls (using ray calls),
                - Otherwise we push states to the Borg shared state
        """
        self.name = name
        self.lock = None
        self.global_items = {}
        self.thread = None
        self.queue = None
        self.global_state = MainState()

        self.locktype = kwargs.get("ltype", "thread")
        self.enqueue = kwargs.get("enqueue", False)
        if self.locktype is "thread":
            self.lock = threading.Lock()
        
        if self.enqueue is True:
            self.queue = MQueue()
            self.thread = threading.Thread(target=self.queued_writer, daemon=True)
            self.thread.start()
    
    def add_global_key(self, addable):
        global_keys = self.global_items.keys()
        addable_name = addable.type_name
        if addable_name not in global_keys:
            self.global_items[addable_name] = []
        addable.reset()
        self.global_items[addable_name].append(addable)
        

    def add(self, addable):
        # Sets an addable object. Checks to be an instance of Session/Executable.
        if isinstance(addable, BaseBlock):
            self.add_global_key(addable)
    
    def queued_writer(self):
        message = None
        queue = self.queue

        try:
            while True:
                message = queue.get()
                if message is None:
                    break

                if isinstance(message, dict) == False:
                    continue
                self.global_state.dispatch(**message)
        except Exception as e:
            print(str(e))
    def stop(self):
        with self.lock:
            if self.enqueue:
                self.queue.put(None)
                self.thread.join()
    
    def send_msg(self, msg):
        if isinstance(msg, dict):
            with self.lock:
                if self.enqueue:
                    self.queue.put(msg)


    def run(self, **kwargs):
        # All Addables should have a name of its own and kwargs
        type_name = kwargs.get("type", None)
        name = kwargs.get("name", None)
        data = kwargs.get("data", None)
        if type_name is None:
            # Type name can be anything
            raise AttributeError("Run type name not found")
        if data is None:
            raise AttributeError("No data supplied. Please supply data to run this process.")
        
        if type_name not in self.global_items.keys():
            raise AttributeError("Type doesn't exist")
        
        else:
            # Run the task graph here using the scheduler
            for _ in self.global_items[type_name]:
                # First check to see if the required are added there
                # Some required items will have defaults in the session __init__
                _.execute()
                

                
    

# Example: Reinforcement Learning


if __name__ == "__main__":
    sess = Session("blank", enqueue=True)
    sess.add(PortfolioBlock("userportfolio"))
    # Allow us to __call__ to add default variables
    sess.add(SARSALearning("qlearning", modloader={}, portfolio={}, environment={}, dispatch={}, modstore={}))
    sess.run(type="reinforcement", name="qlearning", data={})
    sess.stop()


    # Tests to run
    # Can I push an action to modify a state

"""
# The run here would represent the
sess.run(name="qlearning", type="reinforcement", data={"action": 1, dataframe: df})
"""


"""
sess = Session("t1")
sess.add(ReinforcementLearning())
"""