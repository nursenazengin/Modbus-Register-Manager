import os, redis
from dotenv import load_dotenv


rdb = None
load_dotenv()

class ConnectionRedis():
    def connectRedis():
        global rdb
        redisAddress = os.getenv('REDIS_ADDRESS')
        redisPassword = os.getenv('REDIS_PASSWORD')
        redisUsername = os.getenv('REDIS_USERNAME')

        try:
            rdb = redis.StrictRedis(
                host=redisAddress.split(':')[0],
                port=int(redisAddress.split(':')[1]),
                password=redisPassword,
                username=redisUsername, 
                db=0
            )

            pong = rdb.ping()
            print(f"Connected to Redis")

        except redis.ConnectionError as e:
            print(f"Could not connect to Redis: {e}")


    def setRedis(key:str, value:str) -> None:
        if rdb is None:
            print("Redis connection has not been established")

        try:
            rdb.set(key, value)

        except redis.RedisError as e:
            print(f"Redis set error: {e}")


    def getRedis(key: str) -> str:
        try: 
            val = rdb.get(key)
            if val is None:
                return ""
            return str(val, 'utf-8')
        
        
        except redis.RedisError as e:
            print(f"Redis get error {e}")








