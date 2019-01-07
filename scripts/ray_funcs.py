import ray

ray.init()

@ray.remote
def ray_add(a, b):
    return a+b

@ray.remote
class RayOperations(object):
    def __init__(self):
        self.pussy = []
        print("Load from file if we get here")

    def add(self, a, b):
        opt = a + b
        self.pussy.append({"name": "add", "result": opt})
        return opt
    
    def divide(self, a, b):
        opt = a / b
        self.pussy.append({"name": "divide", "result": opt})
        return opt
    
    def multiply(self, a, b):
        opt = a * b
        self.pussy.append({"name": "multiply", "result": opt})
        return opt
    
    def subtract(self, a, b):
        opt = a - b
        self.pussy.append({"name": "subtract", "result": opt})
        return opt