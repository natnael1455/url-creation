from google.cloud import pubsub_v1
from itertools import groupby
import json
import csv


def key_func(key):
    return key["category"]


def csv_read():
    with open("../input/KenyaProduct.csv", encoding="utf-8") as csvf:
        csvReader = csv.DictReader(csvf)
        items = {}
        for key, values in groupby(csvReader, key_func):
            items.update({key: list(values)})
    return items


def publisher_function(data):

    # TODO(developer)
    project_id = "baia-project"
    topic_id = "catalogTopic"

    publisher = pubsub_v1.PublisherClient()
    # The `topic_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/topics/{topic_id}`
    topic_path = publisher.topic_path(project_id, topic_id)

    data = json.dumps(data)
    data = data.encode("utf-8")
    # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, data)
    print(future.result())

    print(f"Published messages to {topic_path}.")


if __name__ == "__main__":
    # publisher_function()
    items = csv_read()
    data = {"name": "selam", "items": items}
    publisher_function(data)
    print(data)
