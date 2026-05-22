import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()
r = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
SESSION_TTL = 1800  # 30 minutes

def save_session(session_id: str, data: dict):
    r.setex(session_id, SESSION_TTL, json.dumps(data))

def get_session(session_id: str) -> dict:
    raw = r.get(session_id)
    if raw:
        return json.loads(raw)
    return {}

def update_session(session_id: str, updates: dict):
    existing = get_session(session_id)
    existing.update(updates)
    save_session(session_id, existing)

def clear_session(session_id: str):
    r.delete(session_id)