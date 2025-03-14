import redis

def get_connect()->redis.Redis:
    return redis.Redis(
        host="localhost",
        port=6379,
        db=0,
    )

