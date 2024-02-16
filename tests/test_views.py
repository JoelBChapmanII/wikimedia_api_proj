import pytest
import wikipedia_api

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


@pytest.fixture
def client():
    app = wikipedia_api.init_app()
    with app.test_client() as client:
        yield client


# Happy path tests
def test_good_months(client, mocker):
    """
    Testing all valid months return correctly. The request to wikipedia is mocked so we aren't reaching out during
    a test.

    Asserts 200 is returned
    Asserts views are returned and it is the correct number
    """
    mock_get = mocker.patch("wikipedia_api.views.views.wikipedia_views_request")
    mock_get.return_value = (
        200,
        {
            "items": [
                {
                    "access": "all-access",
                    "agent": "automated",
                    "article": "Python_(programming_language)",
                    "granularity": "monthly",
                    "project": "en.wikipedia",
                    "timestamp": "2015070100",
                    "views": 19541,
                }
            ]
        },
    )
    for month in VALID_MONTHS:
        response = client.get(
            f"/api/v1/views/Python_(programming_language)/monthly/2016/{month}"
        )
        assert response.status_code == 200
        assert response.json["views"] == 19541


def test_generate_month_dates():
    """
    Tests all valid months and two years and verifies a tuple is returned.

    Asserts a tuple is returned from the generate_month_dates function.
    """
    for year in [2022, 2024]:
        for month in VALID_MONTHS:
            result = wikipedia_api.views.views.generate_month_dates(
                month_name=month, year=year
            )
            assert type(result) == tuple


# Sad path tests
def test_bad_months(client, mocker):
    """
    Tests different invalid months are passed to the API. Asserts the return code is 400 and the error message is as
    expected.

    Asserts 400 is returned from a invalid month
    Asserts the error message is correct
    """
    mocker.patch("wikipedia_api.views.views.wikipedia_views_request")
    for month in ["2000", 2000, "janufebust"]:
        response = client.get(
            f"/api/v1/views/Python_(programming_language)/monthly/2016/{month}"
        )
        assert response.status_code == 400
        assert "Invalid month given" in response.json["Error"]


def test_non_int_year(client, mocker):
    """
    Tests the response and status code if a year is unable to be cast as an int, for example if it is a word.

    Asserts 400 is returned from a invalid year
    Asserts the error message is as expected.
    """
    mocker.patch("wikipedia_api.views.views.wikipedia_views_request")
    response = client.get(
        f"/api/v1/views/Python_(programming_language)/monthly/twothousandtwentytwo/january"
    )
    assert response.status_code == 400
    assert "Unable to cast year as int" in response.json["Error"]


def test_out_of_range_year(client, mocker):
    """
    Tests the response and status code if a year is out of range of the api.

    Asserts 400 is returned from a invalid year
    Asserts the error message is as expected.
    """
    mocker.patch("wikipedia_api.views.views.wikipedia_views_request")
    response = client.get(
        f"/api/v1/views/Python_(programming_language)/monthly/3000/january"
    )
    assert response.status_code == 400
    assert "Year is not valid" in response.json["Error"]
