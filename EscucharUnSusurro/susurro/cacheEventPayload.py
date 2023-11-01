import redis
import numpy as np
from segmenter import *
import segmentedwhisper
from loguru import logger

redisClient = redis.StrictRedis(host='localhost', port=6379, db=6)

#only get unique from list
def unique(listElement):
    x = np.array(listElement)
    
    return np.unique(x)
def cacheEventPayload(payload):
    sessionId = payload["sessionId"]
    recordUrl = payload["recordingUrl"]
     
    key_set = redisClient.setnx(sessionId, recordUrl)

    if key_set:
        logger.info(f"'{sessionId}' set value '{recordUrl}'")

        #define expiry duration to clean redis(one day)

        redisClient.expire(sessionId, 86400)

        #send task to celery que
              #enque a tasl with received audio file
        segmentedwhisper.maintask.delay(recordUrl)
    else:
        logger.info(f"key '{sessionId}' already exists  not set")


