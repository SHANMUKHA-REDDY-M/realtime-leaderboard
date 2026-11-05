import os

import redis


REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
STREAM_KEY = "gaming_events_stream"
LEADERBOARD_KEY = "global_leaderboard"
LAST_ID = "0-0"

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
)

print("Starting real-time stream processor... (Press Ctrl+C to stop)")
try:
    while True:
        # Block for 1000 ms when no new data is available.
        messages = redis_client.xread(
            {STREAM_KEY: LAST_ID},
            count=10,
            block=1000,
        )

        if not messages:
            continue

        for _, event_list in messages:
            for message_id, message_data in event_list:
                username = message_data["username"]
                score = int(message_data["score_earned"])

                # ZINCRBY atomically updates the user's score.
                redis_client.zincrby(LEADERBOARD_KEY, score, username)
                LAST_ID = message_id
                print(
                    f"Processed event {message_id}: "
                    f"updated {username} (+{score})"
                )
except KeyboardInterrupt:
    print("\nStream processing stopped.")
