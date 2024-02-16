FROM python:3.11.3

# Set working dir
WORKDIR /app

# Set up dependencies, I like to do these first so they don't have to be reinstalled when docker layers change
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy app
COPY wikipedia_api wikipedia_api

# Add Configurations for start up
COPY wsgi.py wsgi.py
COPY config.py config.py

# Run the flask app
CMD ["flask", "--app", "wsgi", "run", "-h", "0.0.0.0", "-p", "8080", "--debug", "--with-threads"]
