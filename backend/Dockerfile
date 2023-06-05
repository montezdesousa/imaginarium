# syntax = docker/dockerfile:1.2
# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Load secrets
RUN --mount=type=secret,id=_env,dst=/etc/secrets/.env cat /etc/secrets/.env
COPY /env/secrets/.env ./engine
RUN ls engine

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Train the model
RUN ["python", "-m", "engine.train_knn"]

# As an example here we're running the web service with one worker on uvicorn.
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT} --workers 1