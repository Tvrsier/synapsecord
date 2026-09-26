

class RiotAPIError(Exception):
    def __init__(self, message: str, *, status_code: int | None = None):
        self.status_code = status_code
        super().__init__(message)


class RiotAuthenticationError(RiotAPIError):
    pass


class RiotNotFoundError(RiotAPIError):
    pass


class RiotRateLimitError(RiotAPIError):
    def __init__(self, *, retry_after: float | None = None, status_code: int =429):
        self.retry_after = retry_after
        super().__init__("Riot API rate limit exceeded", status_code=status_code)


class RiotServiceUnavailableError(RiotAPIError):
    pass


class RiotTransportError(RiotAPIError):
    pass


class RiotInvalidResponseError(RiotAPIError):
    pass
