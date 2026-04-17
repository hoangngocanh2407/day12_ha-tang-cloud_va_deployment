import signal
import sys
import logging
import json
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException
import uvicorn
import redis

from .config import settings
from .auth import verify_api_key
from .rate_limiter import check_rate_limit
from .cost_guard import check_budget

from utils.mock_llm import ask 

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "name": record.name
        }
        return json.dumps(log_record)

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
logger.setLevel(settings.LOG_LEVEL)

app = FastAPI(title="Final Production Agent")
r = redis.from_url(settings.REDIS_URL, decode_responses=True)

@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up.")

def shutdown_handler(signum, frame):
    logger.info("Gracefully shutting down...")
    r.close()
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown_handler)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ready")
def ready():
    try:
        r.ping()
        return {"status": "ready"}
    except Exception as e:
        logger.error(f"Redis connection failed: {e}")
        raise HTTPException(status_code=503, detail="Service not ready")

class AskRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_endpoint(
    request: AskRequest,
    user_id: str = Depends(verify_api_key),
):
    check_rate_limit(user_id)
    check_budget(user_id, estimated_cost=0.01)
    
    # Stateless design (conversation history in Redis)
    history_key = f"history:{user_id}"
    history = r.lrange(history_key, 0, -1)
    
    answer = ask(request.question)
    
    r.rpush(history_key, f"Q: {request.question}")
    r.rpush(history_key, f"A: {answer}")
    r.expire(history_key, 3600)
    
    logger.info(f"Processed request for {user_id}")
    return {"answer": answer, "history_len": len(history) // 2 + 1}
