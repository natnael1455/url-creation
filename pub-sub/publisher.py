from google.cloud import pubsub_v1
import json

# TODO(developer)
project_id = "baia-project"
topic_id = "catalogTopic"

publisher = pubsub_v1.PublisherClient()
# The `topic_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/topics/{topic_id}`
topic_path = publisher.topic_path(project_id, topic_id)

js = {"name": "selam"}
data = json.dumps(js)
data = data.encode("utf-8")
# When you publish a message, the client returns a future.
future = publisher.publish(topic_path, data)
print(future.result())

print(f"Published messages to {topic_path}.")
