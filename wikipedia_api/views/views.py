"""General page routes."""

# Flask imports
from flask import Blueprint
from flask import current_app as app

# Used to hit wiki's rest endpoint
import requests

# Used to determine the start and end of the month
from datetime import datetime, timedelta
import calendar

# Blueprint Configuration
views = Blueprint("views", __name__)

# Constants
BASE_URL = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{app.config['WIKIPEDIA_PROJECT']}"
VALID_MONTHS = [
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
]


def generate_month_dates(month_name: str, year: int) -> tuple:
    """
    This function takes a month "january, july, august, etc." a year and transforms that to
    the start of the month and the end of the month in YYYYMMDD format. This is needed
    because wikipedia uses that in it's view count rest API URL.

    :returns: tuple
    """
    # Convert month name to a numeric month
    month_number = list(calendar.month_name).index(month_name.capitalize())
    # Get the first day of the month
    start_date = datetime(year, month_number, 1).strftime("%Y%m%d")
    # Get the last day of the month
    last_day = calendar.monthrange(year, month_number)[1]
    # Get the end date
    end_date = datetime(year, month_number, last_day).strftime("%Y%m%d")
    return start_date, end_date


def wikipedia_views_request(endpoint: str) -> tuple[str, dict]:
    """
    This function takes in the endpoint URL and sends a get request to the wiki site
    then returns the response code and either an error message or the response from wikipedia.
    Having this wrapped in a function makes testing easier.

    :returns: tuple[str, dict]
    """
    # Send the response to wikipedia
    response = requests.get(
        f"{BASE_URL}/{endpoint}",
        headers={"User-Agent": app.config["USER_AGENT"], "accept": "application/json"},
    )
    data = response.json()
    return (response.status_code, data)


# See the wikimedia API examples here:
# https://wikimedia.org/api/rest_v1/#/Pageviews%20data/get_metrics_pageviews_per_article__project___access___agent___article___granularity___start___end_
@views.route("/api/v1/views/<article>/monthly/<year>/<month>", methods=["GET"])
def monthly_views(article: str, month: str, year: str) -> dict:
    """
    Returns the monthly view metrics endpoint provided the month and the article title as JSON/Dict.

    :returns: JSON
    """
    # Normalize data
    month_name = month.lower()
    try:
        year_int = int(year)
    except ValueError as e:
        return ({"Error": f"Unable to cast year as int: {year}"}, 400)
    except Exception as e:
        return (
            {"Error": f"Unhandled exception caught casting year as int: {year}"},
            400,
        )

    # Verify the month is valid
    if month_name not in VALID_MONTHS:
        return ({"Error": f"Invalid month given: {month}"}, 400)

    # Verify year is valid, 2015 was the earliest year I could query
    if not 2015 <= year_int <= (datetime.now().year):
        return ({"Error": f"Year is not valid: {year_int}"}, 400)

    # Get the start and end date of the provided month and year
    start_date, end_date = generate_month_dates(month, year_int)

    # Get the wikipedia request and return the response
    endpoint = f"all-access/automated/{article}/monthly/{start_date}/{end_date}"
    status_code, data = wikipedia_views_request(endpoint=endpoint)

    # Return either a success or a failure
    if status_code == 200:
        return (
            {"views": data["items"][0]["views"]},
            status_code,
            {"Content-Type": "application/json"},
        )
    else:
        return (
            status_code,
            {
                "Error": data,
                "Further_Information": "https://www.mediawiki.org/wiki/API:REST_API/Status_codes",
            },
        )
