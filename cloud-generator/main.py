# noqa: WPS202
import csv
import sys
from itertools import groupby
from google.cloud import storage
import base64
import os
import click
from jinja2 import Environment, PackageLoader, select_autoescape
from concurrent.futures import TimeoutError
import json
from flask import Flask, request


app = Flask(__name__)

project_id = "baia-project"
subscription_id = "catalogSub"

sys.tracebacklimit = 0


def product_section(index, row):
    env1 = Environment(loader=PackageLoader("main"), autoescape=select_autoescape())
    template = env1.get_template("item.html")
    row1 = False
    row2 = False
    print(index)
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


def head_check(csvreader):
    headercheck = [
        "Name",
        "category",
        "Unit price",
        "Currency",
        "Short code",
        "Description",
        "URL / image",
    ]
    header = []
    header = next(csvreader)
    if set(headercheck).issubset(set(header)):
        click.echo("header muches the format")
    else:
        raise Exception("header of the csv file does not match the format")
    return header


def csv_body(header, file_csv):
    people_list = []
    headers_list = []

    index = 0
    for line in file_csv:

        if index > 0:
            people_dict = {}
            for idx, elem in enumerate(headers_list):
                people_dict[elem] = line[idx]
            people_list.append(people_dict)
        else:
            headers_list = header
        index += 1
    click.echo("dictionary's body created")
    return people_list


def category_section(key, category_data):
    env1 = Environment(loader=PackageLoader("main"), autoescape=select_autoescape())
    template = env1.get_template("category.html")
    pro_section = ""
    for index, row in enumerate(category_data):
        print(index, "-", row)
        pro_section = pro_section + product_section(index, row)
    return template.render(CategoryName=key, item=pro_section)


def key_func(key):
    return key["category"]


def read_csv(file):
    with open(file) as file_csv:
        click.echo(file + " is opened")
        csvreader = csv.reader(file_csv)
        header = head_check(csvreader)
        return csv_body(header, csvreader)


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
        data = json.loads(name)
        generate(data)
        return ("", 204)


if __name__ == "__main__":
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080
