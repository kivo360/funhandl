from funhandler.blocks import ActionBlock
from loguru import logger
from random import choice

class DispatchOrder(ActionBlock):
    def __init__(self, name, **kwargs):
        super().__init__(name, "dispatchorder", **kwargs)
        self.dispatch_type = kwargs.get("dispatch_type", "loop")    
    
    def __call__(self, **kwargs):
        pass
    
    def add_requirements(self, *args):
        return super().add_requirements(*args)
    
    def check_required(self):
        logger.success(self.required)
    
    def action_filter(self):
        logger.debug("Action Filter")

    def reset(self):
        logger.debug("Reset Dispatcher")

    def step(self, action, **kwargs):
        logger.debug("Step through dispatcher {action}, {}", self.dispatch_type, action=action)


if __name__ == "__main__":
    dispatch = DispatchOrder("Live Dispatcher")
    dispatch.reset()
    for i in range(10):
        dispatch.step(choice(["buy", "sell"]))
