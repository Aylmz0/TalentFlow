#!/bin/bash
set -e

echo "=== TalentFlow Deployment Started ==="

# Go to project directory
cd ~/TalentFlow

# Virtual environment setup
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing requirements..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Restart Django in tmux
echo "Managing tmux session..."
if tmux has-session -t talentflow 2>/dev/null; then
  echo "Existing tmux session 'talentflow' found. Restarting..."
  tmux send-keys -t talentflow:0 C-c Enter
  sleep 2
  tmux send-keys -t talentflow:0 "source .venv/bin/activate" Enter
  tmux send-keys -t talentflow:0 "python manage.py runserver 0.0.0.0:8000" Enter
else
  echo "No active tmux session. Creating new session 'talentflow'..."
  tmux new-session -d -s talentflow "source .venv/bin/activate && python manage.py runserver 0.0.0.0:8000"
fi

echo "=== Deployment Successfully Completed! ==="
