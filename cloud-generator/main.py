import base64
import json
import os

import click
from flask import Flask, request
from google.cloud import storage
from jinja2 import Environment, PackageLoader, select_autoescape

app = Flask(__name__)


def product_section(index, row):
    env1 = Environment(loader=PackageLoader("main"), autoescape=select_autoescape())
    template = env1.get_template("item.html")
    row1 = False
    row2 = False
    if (index % 2) == 0:
        row1 = True
    else:
        row2 = True

    product_name = row["Name"]
    unit_price = row["Unit price"]
    currency = row["Currency"]
    code = row["Short code"]
    img = row["URL / image"]

    return template.render(
        row1=row1,
        row2=row2,
        ItemName=product_name,
        UnitPrice=str(unit_price),
        currency=currency,
        ShortCode=code,
        img=img,
    )


def category_section(key, category_data):
    env1 = Environment(loader=PackageLoader("main"), autoescape=select_autoescape())
    template = env1.get_template("category.html")
    pro_section = ""
    for index, row in enumerate(category_data):
        pro_section = pro_section + product_section(index, row)
    return template.render(CategoryName=key, item=pro_section)


def create_html(file, data):
    click.echo("creating " + file)
    env = Environment(loader=PackageLoader("main"), autoescape=select_autoescape())
    template = env.get_template("index.html")
    with open("output/" + file, "w") as htmls_file:

        middle = ""
        for key, value in data.items():
            middle = middle + category_section(key, value)

        htmls_file.write(template.render(category=middle))
        click.echo(file + " created")
        htmls_file.close()


def upload_file(blobname):
    storage_client = storage.Client()
    bucket = storage_client.bucket("baia-catalogs")
    for filename in os.listdir("output"):
        blob = bucket.blob(blobname + "/" + filename)
        blob.upload_from_filename("output/" + filename)


def generate(data):
    click.echo("trying to open " + "product.csv")
    try:
        create_html("index.html", data["items"])
        upload_file(data["name"])
    except FileNotFoundError:
        click.echo("product.csv" + " not found in input directory")
    except Exception as ex:
        click.echo(ex)


@app.route("/", methods=["POST"])
def index():
    envelope = request.get_json()
    if not envelope:
        msg = "no Pub/Sub message received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    pubsub_message = envelope["message"]

    name = "World"
    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        name = base64.b64decode(pubsub_message["data"]).decode("utf-8").strip()
        name = json.loads(name)

        generate(name)
    print(name)

    return ("", 204)


if __name__ == "__main__":
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080
    app.run(host="0.0.0.0", port=PORT, debug=True)
