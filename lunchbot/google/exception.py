"""Exceptions and exception utilities related to Google API calls."""


def handle_bad_response(response):
        """Raise the appropriate error for given response status."""
        status = response['status']
        error_message = response.get('error_message')
        if status == 'ZERO_RESULTS':
            raise GoogleZeroResults(error_message)
        elif status == 'OVER_QUERY_LIMIT':
            raise GoogleOverQueryLimit(error_message)
        elif status == 'REQUEST_DENIED':
            raise GoogleRequestDenied(error_message)
        elif status == 'INVALID_REQUEST':
            raise GoogleInvalidRequest(error_message)
        elif status == 'UNKNOWN_ERROR':
            raise GoogleUnknownError(error_message)


class GoogleGeocodingException(Exception):
    pass


class GoogleZeroResults(Exception):
    pass


class GoogleOverQueryLimit(Exception):
    pass


class GoogleRequestDenied(Exception):
    pass


class GoogleInvalidRequest(Exception):
    pass


class GoogleUnknownError(Exception):
    pass
