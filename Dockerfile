FROM python:3-slim

# prepare environment
WORKDIR /app
COPY . /app
RUN python3 -m pip install -r requirements.txt

# setup CMD
CMD [ "python3", "app.py" ]
