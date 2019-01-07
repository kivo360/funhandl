import ray
import random
from sanic import Sanic
from sanic.response import json

from ray_funcs import ray_add, RayOperations

ray_ops = RayOperations.remote()

app = Sanic()

@app.route("/ray/add", methods=['POST'])
async def test(request):
    r = request.json
    if r is None:
        return json({"msg": "Please ensure that you send in a json"}, status=500)
    print(r)
    if r["operation"] == "add":
        ret = ray_ops.add.remote(r["a"], r["b"])
        # ray_ops.add_list_item.remote("add")
        return json({"msg": "We called a function.", "answer": ray.get(ret), "lis":ray.get(ray_ops.get_list_items.remote())})
    elif r["operation"] == "subtract":
        ret = ray_ops.subtract.remote(r["a"], r["b"])
        # ray_ops.add_list_item.remote("subtract")
        return json({"msg": "We called a function.", "answer": ray.get(ret), "lis":ray.get(ray_ops.get_list_items.remote())})
    elif r["operation"] == "multiply":
        ret = ray_ops.multiply.remote(r["a"], r["b"])
        # ray_ops.add_list_item.remote("multiply")
        return json({"msg": "We called a function.", "answer": ray.get(ret), "lis":ray.get(ray_ops.get_list_items.remote())})
    elif r["operation"] == "divide":
        ret = ray_ops.divide.remote(r["a"], r["b"])
        # ray_ops.add_list_item.remote("divide")
        return json({"msg": "We called a function.", "answer": ray.get(ret), "lis":ray.get(ray_ops.get_list_items.remote())})
    return json({"hello": "world"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)