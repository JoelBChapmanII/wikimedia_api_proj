# Overview

This is a small flask api demonstrating the use of flask in a modularized method to build an API for querying information
from wikimedia/wikipedia. Docker and docker compose are used to show how this app can easily be packaged and ran.

## Prerequisites

- [Docker](https://docs.docker.com/engine/install/)

## Project Structure

This project uses flask blueprints to allow for easy additions and compartmentalizing routes and api endpoints. To add a
new API path create a new directory under [wikipedia_api](./wikipedia_api/) and register the blueprint in
[init_app](./wikipedia_api/__init__.py). See the [wikipedia_api/views](./wikipedia_api/views/) as an example.

```bash
├── Dockerfile # The dockerfile used to build this application
├── README.md
├── config.py # Configurations for the application
├── docker-compose-dev.yml # A development focused docker compose file
├── docker-compose.yml # A docker compose file to run the application without the intent of testing, updating, development
├── requirements.txt # The dependencies for the application
├── tests # The directory where tests are kept
├── wikipedia_api # The main application directory where the api code resides
└── wsgi.py # The entry point used to initialize and start the application
```

## Deployment

To run this application first build the docker container using:

```bash
docker compose build
```

Then run the container by issuing:

```bash
# Optionally to run in the background pass -d for detached
docker compose up
```

To stop the container and its processes run:

```bash
docker compose down
```

__Note:__ It would be best to eventually publish this to a registry but this work for a demonstration.

## Usage

For usage it is assumed that the container is running as directed in the [Deployment Section](#deployment).

This api allows for three inputs, the article in question, the year, and the month. The article name parameter is the
same as you would see in your address bar when you navigate to the wikipedia articles page. The year parameter is in
YYYY format. The month parameter is by name, for example january, february, march, etc.

Issuing an API call:

```bash
# Parameterized Example
curl "localhost:8080/api/v1/views/<ARTICLE>/monthly/<YEAR>/<MONTH>"

# Filled in example
curl "localhost:8080/api/v1/views/Python_(programming_language)/monthly/2022/july"
```

Output from the API is a json object in the format of "{"views": "1000"}" or in the case of an error
"{"Error": "Error message"}".

## Development

### Development Prerequisites

- [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)
    - This is optional but used to version the version of python used for this project

### Live Local Development Using Docker

To run this container live and have it pick up changes build the container and run docker compose specifying the
development docker-compose file. The wikipedia_api directory is mounted as a volume and flask picks up changes allowing
easy development and debugging.

```bash
docker build . -t wikiwrapperdev

# Optionally pass -d, but not passing -d give a live terminal with logs
docker compose -f docker-compose-dev.yml up
```

### Unit Testing

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate virtual environment if not already active
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run pytest
pytest
```

### Linting

This project uses [black](https://github.com/psf/black) to provide opinionated and hands off formatting for python code
style.

To format your code simply run:
```bash
black .
```

## Post Development Thoughts

For a prod environment I'll need to use a different wsgi package and would probably want a load balancer technology like
haproxy or nginx.

I know in the instructions it didn't ask for a year to be passed but I assumed we may want to go back and not always use
the current year. Maybe a future revision is to have a default for the current year.

The requirements file could be split up into environments (development/(staging/production/QA)) depending on need since I
don't need the development installed packages when the container is running the app.

Adding a package for test coverage would be nice to have.

Ideally github actions or another CI/CD tooling would lint, run unit tests, and publish to a container registry.

For a production deployment we would want to run over port 443 and redirect 80 to 443. This would be fairly easy with
haproxy or nginx.

If I were going to add additional routes to this API I would most likely update the usage section or create a new
markdown file that goes into more detail into each route. Also using an auto documentation dependency would be nice.
