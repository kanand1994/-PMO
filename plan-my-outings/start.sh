#!/bin/bash
cd backend
gunicorn app:app --host 0.0.0.0 --port $PORT