#!/usr/bin/env bash
gunicorn adventure.wsgi:application --bind 0.0.0.0:$PORT