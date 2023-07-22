# Kafka with docker compose
https://kafka.apache.org/quickstart-docker

All of Kafka's command line tools have additional options: run the kafka-topics.sh command without any arguments to display usage information.

### Setup and run the environment
`docker-compose -f kafka-docker-compose.yml up`

### create a topic:

`$ docker exec -it kafka-broker kafka-topics.sh --create --topic thomas-events`

### Write events:
Run the console producer client to write a few events into your topic. By default, each line you enter will result in a separate event being written to the topic.

```
$ docker exec -it kafka-broker kafka-console-producer.sh --topic quickstart-events
This is my first event
This is my second event
```
You can stop the producer client with Ctrl-C at any time.