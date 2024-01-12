from confluent_kafka import KafkaError, KafkaException, Consumer
import sys
import json

from cacheEventPayload import cacheEventPayload
from loguru import logger


running = True
def consumeCompletedCalls():

    #define configuration
    conf = {
        'bootstrap.servers':"", #Enter Server address, 
        'group.id': '',
        'auto.offset.reset': 'smallest',
        'broker.address.family': 'v4',
    
    }

    #instantiate a consumer
    consumer = Consumer(conf)
    

    topics = ["completedTpc"]


    try:
        logger.info("Subscribing to {} ".format(topics))
        consumer.subscribe(topics)
        logger.info("Subscribed to {} ".format(topics))
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
                logger.info("Found url {}".format(recordingUrl))
                
                if len(recordingUrl) >=10:
                    #write to temp cache to enforce uniqueness
                    cacheEventPayload(jsonString)

               
                else:
                    logger.debug("Error with audio url {}".format(recordingUrl))
    finally:
        #close down consumer
        consumer.close()




if __name__ == "__main__":
    consumeCompletedCalls()
