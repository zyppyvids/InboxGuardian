import json
import time
from kafka import KafkaProducer, KafkaConsumer
from models_evaluator import Evaluator

EVALUATE_REQUEST_KAFKA_TOPIC = 'evaluate_request'
EVALUATE_CONFIRMED_KAFKA_TOPIC = 'evaluate_confirmed'

def get_items():
    print("Creating evaluator...")
    evaluator = Evaluator()

    print("Creating evaluator's consumer and producer...")
    consumer = KafkaConsumer(
        EVALUATE_REQUEST_KAFKA_TOPIC,
        bootstrap_servers='kafka:9092',
        api_version=(2, 0, 2)
        )
    
    producer = KafkaProducer(
        bootstrap_servers='kafka:9092',
        api_version=(2, 0, 2)
        )

    return (evaluator, consumer, producer)

def main():
    # Creates the evaluator, consumer and producer
    evaluator, consumer, producer = get_items()

    while True:
        for message in consumer:
            try:
                print("Ongoing evaluation...")
                
                # Casts the message to a dictionary
                consumed_message = json.loads(message.value.decode())
                print(f"Doing evaluation on {consumed_message}.")

                # Gets the text from the consumed message
                text = consumed_message['text']
                
                # Calls the evaluator on the passed text
                result = evaluator.evaluate(text)

                # Creates the data dictionary
                data = {
                    'text': text,
                    'result': result 
                }

                print(f"The result is {result}.")

                # Sends the recently created dictionary containing the result
                producer.send(
                    EVALUATE_CONFIRMED_KAFKA_TOPIC,
                    json.dumps(data).encode('utf-8')
                )
            except Exception as error:
                print(f"Exception was caught while evaluation: {error}")

if __name__ == '__main__':
    main()