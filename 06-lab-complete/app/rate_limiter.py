import redis
import time
from fastapi import HTTPException
from .config import settings

r = redis.from_url(settings.REDIS_URL, decode_responses=True)

def check_rate_limit(user_id: str):
    now = int(time.time())
    window_start = now - 60
    key = f"rate_limit:{user_id}"
    
    pipe = r.pipeline()
    pipe.zremrangebyscore(key, 0, window_start) # remove old requests
    pipe.zcard(key) # count current requests
    pipe.zadd(key, {str(now): now}) # add new request
    pipe.expire(key, 60) # set expiry
    results = pipe.execute()
    
    current_count = results[1]
    
    if current_count >= settings.RATE_LIMIT_PER_MINUTE:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
