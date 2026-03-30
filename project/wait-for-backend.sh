#!/bin/sh

echo "Waiting for backend..."
while ! nc -z backend 8001; do
  sleep 0.2
done
echo "Backend is up!"
nginx -g 'daemon off;'