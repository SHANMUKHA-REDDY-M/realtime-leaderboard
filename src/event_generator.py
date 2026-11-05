import os
import random
import time

import redis
from faker import Faker


REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
STREAM_KEY = "gaming_events_stream"

fake = Faker()
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
)

# Pre-generate user profiles to simulate returning players.
users = [
    {"user_id": f"U{i:04d}", "username": fake.user_name()}
    for i in range(1, 51)
]

print("Starting real-time event generator... (Press Ctrl+C to stop)")
try:
    while True:
        user = random.choice(users)
        event = {
            "event_id": fake.uuid4(),
            "user_id": user["user_id"],
            "username": user["username"],
            "score_earned": random.randint(10, 500),
            "timestamp": time.time(),
        }

        # XADD pushes the event to the Redis Stream, like Kinesis PutRecord.
        redis_client.xadd(STREAM_KEY, event)
        print(f"Published: {user['username']} earned {event['score_earned']} pts")
        time.sleep(random.uniform(0.1, 0.5))
except KeyboardInterrupt:
    print("\nEvent generation stopped.")
