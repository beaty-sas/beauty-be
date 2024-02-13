from beauty_be.conf.settings import settings

JWK_URL = '/'.join([settings.AUTH0_URL.rstrip('/'), '.well-known/jwks.json'])
JWT_ACCESS_TOKEN_ALGORITHMS = ['RS256']

BASE_HTTP_CLIENT_TIMEOUT: float = 3.0

GOOGLE_MAPS_BASE_URL = 'https://maps.googleapis.com'
DEFAULT_SRID = 102013  # Europe


class ErrorMessages:
    DO_NOT_HAVE_PERMISSIONS = 'You don\'t have permission.'
    OBJECT_NOT_FOUND = '{object_type} with ID #{id} not found.'

    NOT_AUTH = 'Not authenticated.'
    INVALID_TOKEN = 'Invalid token.'
    NOT_ENOUGH_PERMISSIONS = 'Not enough permissions.'
