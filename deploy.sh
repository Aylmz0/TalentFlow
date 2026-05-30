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
  echo "Existing tmux session 'talentflow' found. Stopping..."
  tmux kill-session -t talentflow
  sleep 1
fi

echo "Creating new tmux session 'talentflow'..."
tmux new-session -d -s talentflow ".venv/bin/python manage.py runserver 0.0.0.0:8000"

echo "=== Deployment Successfully Completed! ==="
