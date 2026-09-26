from synapsecord_core.integration.riot import RiotAPIError, RiotRateLimitError


def test_api_error_preserves_status_code():
    error = RiotAPIError(
        "failure",
        status_code=500,
    )

    assert error.status_code == 500
    assert str(error) == "failure"

def test_rate_limited_error_preserves_retry_after():
    error = RiotRateLimitError(
        retry_after=2.5
    )

    assert error.status_code == 429
    assert error.retry_after == 2.5
    assert str(error) == "Riot API rate limit exceeded"