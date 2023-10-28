from confluent_kafka import KafkaError, KafkaException, Consumer
import sys
import json

from cacheEventPayload import cacheEventPayload


running = True
def consumeCompletedCalls(consumer, topics):

    try:
        consumer.subscribe(topics)
        while running:
            msg = consumer.poll(timeout=1.0)
            if msg is None: continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    #End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                valueString = str(msg.value(), encoding='utf-8')
                jsonString = json.loads(valueString)
                recordingUrl = jsonString["recordingUrl"]
                print("Found url {}".format(recordingUrl))
                
                if len(recordingUrl) >=10:
                    #write to temp cache to enforce uniqueness
                    cacheEventPayload(jsonString)

               
                else:
                    print("Error with audio url {}".format(recordingUrl))
    finally:
        #close down consumer
        consumer.close()



#define configuration
conf = {
    'bootstrap.servers': 'localhost:9092', 
    'group.id': 'Muchmi-ML',
    'auto.offset.reset': 'smallest',
}

#instantiate a consumer
consumer = Consumer(conf)

topics = ["completedTpc"]


if __name__ == "__main__":
    consumeCompletedCalls(consumer=consumer, topics=topics)
