#!/bin/bash

# Upgrade pip first
python3 -m pip install --upgrade pip setuptools wheel

# Install lightweight packages first
python3 -m pip install -r requirements.txt

# Install ML packages separately to avoid memory issues
python3 -m pip install -r requirements-ml.txt

# Start FastAPI using Uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 7860