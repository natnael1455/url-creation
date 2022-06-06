from functools import reduce
from os import environ

from flask import Flask, redirect, request

app = Flask(__name__)


def payload_creator(product):

    items = reduce(
        lambda x, key: x + "_" + key[0] + "_" + key[1] if int(key[1]) != 0 else x,
        product.items(),
        "",
    )

    return items[1:]


def url_creator(product):
    payload = payload_creator(product)

    uri = environ.get("uri")

    if payload == "":
        url = "error"
    else:
        url = uri + payload
    return url


@app.route("/api", methods=["POST"])
def process_form_data():
    product = request.form
    if url_creator(product) == "error":
        return "no item is selected", 400
    else:
        return redirect(url_creator(product), code=302)


if __name__ == "__main__":
    app.run(debug=True)
