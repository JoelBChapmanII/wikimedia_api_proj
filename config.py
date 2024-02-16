"""Flask App configuration."""

from os import environ, path

# Specificy a `.env` file containing key/value config values
basedir = path.abspath(path.dirname(__file__))


class Config:
    """Set Flask config variables."""

    # General Config
    WIKIPEDIA_PROJECT = "en.wikipedia.org"
    USER_AGENT = "JoelChapmanGrowTherapyFlaskApp/0.1 (joelbchapmanii@gmail.com)"
    ENVIRONMENT = "development"
