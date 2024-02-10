import json
from django.http import Http404
from typing import List
from ninja import Router, Schema
from asgiref.sync import sync_to_async
from kafka import KafkaConsumer, KafkaProducer

evaluateRouter = Router()

EVALUATE_REQUEST_KAFKA_TOPIC = 'evaluate_request'
EVALUATE_CONFIRMED_KAFKA_TOPIC = 'evaluate_confirmed'

consumer = KafkaConsumer(
        EVALUATE_CONFIRMED_KAFKA_TOPIC,
        bootstrap_servers='kafka:9092',
        api_version=(2, 0, 2)
        )
    
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    api_version=(2, 0, 2)
    )

class EvaluateResult():
    def __init__(self, text: str, result: bool):
        self.text = text
        self.result = result

class EvaluateResultDto(Schema):
    text: str
    result: bool

class Evaluate:
    @evaluateRouter.get("", response = EvaluateResultDto)
    def evaluateText(request, text: str):
        # Creates the data dictionary
        data = {
            'text': text
        }

        # Sends the recently created dictionary containing the result
        producer.send(
            EVALUATE_REQUEST_KAFKA_TOPIC,
            json.dumps(data).encode('utf-8')
        )

        for message in consumer:
            # Casts the message to a dictionary
            consumed_message = json.loads(message.value.decode())
            print(f"Doing evaluation on {consumed_message}.")

            # Gets the text from the consumed message
            result = consumed_message['result']

            # Creates the returnable dto
            returnable = EvaluateResult(text, result)

            print(f"The dto is {returnable.text} - {returnable.result}.")
            
            return returnable