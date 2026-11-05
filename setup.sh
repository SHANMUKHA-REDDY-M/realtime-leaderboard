#!/bin/bash
set -e

echo "Setting up Real-Time Streaming & NoSQL Leaderboard..."

python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt

echo "Setup complete. Start Redis with: docker compose up -d"
echo "Then run the processor, dashboard, and generator in separate terminals."
