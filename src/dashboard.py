import os
import time

import redis


REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
LEADERBOARD_KEY = "global_leaderboard"

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
)


def print_leaderboard() -> None:
    # ZREVRANGE returns the highest scores first in O(log(N) + K) time.
    top_players = redis_client.zrevrange(
        LEADERBOARD_KEY,
        0,
        9,
        withscores=True,
    )

    print("\n" + "=" * 30)
    print("LIVE GLOBAL LEADERBOARD")
    print("=" * 30)

    if not top_players:
        print("Waiting for data...")
    else:
        for rank, (username, score) in enumerate(top_players, 1):
            print(f"#{rank:02d} | {username.ljust(15)} | {int(score):,} pts")
        print("=" * 30)


if __name__ == "__main__":
    try:
        while True:
            print_leaderboard()
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nDashboard closed.")
