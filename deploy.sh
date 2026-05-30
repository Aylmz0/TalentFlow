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

# Restart Django in tmux (Guaranteed to run in bash regardless of default login shell)
echo "Managing tmux session..."
if tmux has-session -t talentflow 2>/dev/null; then
  echo "Stopping existing tmux session 'talentflow'..."
  tmux kill-session -t talentflow
  sleep 1
fi

echo "Creating new tmux session 'talentflow' running bash..."
tmux new-session -d -s talentflow -n "django" bash
sleep 1
tmux send-keys -t talentflow:django "source .venv/bin/activate" Enter
tmux send-keys -t talentflow:django "python manage.py runserver 0.0.0.0:8000" Enter

echo "=== Deployment Successfully Completed! ==="
