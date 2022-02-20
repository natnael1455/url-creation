from os import environ

import click
from flask import Flask, redirect, render_template, request

app = Flask(__name__)


def payload_creator(product):
    start = True
    payload = ""
    for key, value in product.items():
        if int(value) != 0:
            if start:
                payload = key + "_" + value
                start = False
            else:
                payload = payload + "_" + key + "_" + value
        if start:
            payload = "error"
    return payload


def url_creator(product):
    payload = payload_creator(product)
    uri = "https://t.me/kamata_test_bot?start=o_x"
    click.echo(environ.get("url"))
    if payload == "error":
        url = "error"
    else:
        url = uri + payload
    return url


@app.route("/")
def hello():

    # prints parent directory
    return render_template("advanced.html")


@app.route("/", methods=["POST"])
def process_form_data():
    product = request.form
    if url_creator(product) == "error":
        return "no item is selected", 400
    else:
        return redirect(url_creator(product), code=302)


if __name__ == "__main__":
    app.run(debug=True)
