import csv
import json
from itertools import groupby

import click
from google.cloud import pubsub_v1


def key_func(key):
    return key["category"]


def csv_reader(user_name, csv_file):
    services = {}
    with open("../input/" + csv_file, "r") as file:
        csv_data = csv.DictReader(file)
        for category, service in groupby(csv_data, key_func):
            services[category] = list(service)
    return {"name": user_name, "items": services}


def my_publisher(js):
    project_id = "telegram-project-350609"
    topic_id = "catalog-topic"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    data = json.dumps(js)
    data = data.encode("utf-8")
    future = publisher.publish(topic_path, data)
    click.echo(future.result())
    click.echo(f"Published messages to {topic_path}.")


@click.option(
    "--csv_file",
    default="product.csv",
    help="""The csv file from where the html file
    will be generated defult is product.csv""",
)
@click.option(
    "--user_name",
    required=True,
    help="""The owner of the catalog""",
)
@click.command()
def main(user_name, csv_file):
    js = csv_reader(user_name, csv_file)
    my_publisher(js)


if __name__ == "__main__":
    main()
