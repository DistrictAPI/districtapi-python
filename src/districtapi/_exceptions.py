class DistrictAPIError(Exception):
    def __init__(self, message: str, status_code: int | None = None, code: str | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.code = code


class NotFoundError(DistrictAPIError):
    pass


class AuthenticationError(DistrictAPIError):
    pass


class RateLimitError(DistrictAPIError):
    pass


class InvalidParamsError(DistrictAPIError):
    pass
