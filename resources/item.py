import uuid
from flask import request
from flask.views import MethodView #se utiliza para crear una clase y los metodos especificos (dirigidos a un endpoint?
from flask_smorest import Blueprint, abort
from db import items, stores
blp=Blueprint("items", __name__, description="Operations with items")
@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def update(self,item_id):
        item_data = request.get_json()
        if (
                "price" not in item_data
                or "name" not in item_data
        ):
            abort(400, message="Bad request")
        try:
            item = items[item_id]
            item |= item_data  # esto es algo nuevo cualquiera que haya en item data lo va a reemplazar por el item_data
            return item
        except KeyError:
            abort(404, message="Item not found")

    def delete(self,item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted"}
        except KeyError:
            abort(404, message="Item not found")
@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}


    def post(self):
        item_data = request.get_json()
        if (
                "price" not in item_data
                or "store_id" not in item_data
                or "name" not in item_data
        ):
            abort(404, message="Bad requeest. Ensure ´price´,'store_id', and 'name' are included in the JSON paylpoad")
        for item in items.values():
            if (
                    item_data["name"] == item["name"]
                    and item_data["store_id"] == item["store_id"]
            ):
                abort(400, message="item already exists")

        if item_data["store_id"] not in stores:
            abort(404, message="Store not Found.")
        else:
            item_id = uuid.uuid4().hex
            item = {**item_data, "id": item_id}
            items[item_id] = item
            return item, 201


