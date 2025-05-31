import redis
import json
import uuid
from datetime import datetime
from config import REDIS_HOST, REDIS_DB, REDIS_PORT


# Initialize Redis client

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True
)


# Helper Functions: ID Generation


def generate_thread_id() -> str:
    """Generates a new UUID-based thread ID."""
    return str(uuid.uuid4())

def generate_doc_id(source_name: str, file_format: str) -> str:
    """Generates a document ID using source, format, and a unique suffix."""
    return f"{file_format.lower()}_{source_name}_{uuid.uuid4().hex[:6]}"


# Core Function: Logging to Memory


def memory_log(entry: dict, doc_id: str = None, thread_id: str = None):
    """
    Logs or updates a document in Redis memory.
    Creates a new document ID and/or thread ID if not provided.
    
    Args:
        entry (dict): The data to store.
        doc_id (str): Optional. The ID of the document to update.(will create a new one if not given)
        thread_id (str): Optional. The ID of the thread to associate the document with.(will create a new one if not given)

    Returns:
        Tuple (doc_id, thread_id): Final document and thread IDs used.
    """
    new_entry = False

    # Create doc_id if not provided
    if not doc_id:
        doc_id = generate_doc_id(entry.get("source", "unknown"), entry.get("format", "unknown"))
        new_entry = True

    # Create thread_id if not provided
    if not thread_id:
        thread_id = generate_thread_id()

    # Attach metadata
    entry["timestamp"] = datetime.utcnow().isoformat()
    entry["thread_id"] = thread_id

    # Redis key pattern
    redis_key = f"doc:{doc_id}"

    # Store each key-value pair (serialize complex types)
    for k, v in entry.items():
        r.hset(redis_key, k, json.dumps(v) if isinstance(v, (dict, list)) else v)

    # If it's a new document, add to thread list
    if new_entry:
        r.rpush(f"thread:{thread_id}", redis_key)

    return doc_id, thread_id



