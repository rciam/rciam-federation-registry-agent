from requests_oauthlib import OAuth2Session

"""Refreshing an OAuth 2 token using a refresh token.
:param issuer: The token endpoint, must be HTTPS.
:param refresh_token: The refresh_token to use.
:param client_id: Client id obtained during registration
:param client_secret: Client secret obtained during registration
:return: An access token
"""


def refreshTokenGrant(issuer, refreshToken, clientId, clientSecret):
    tokenUrl = issuer + "/token"

    extra = {"client_id": clientId, "client_secret": clientSecret}

    try:
        print('Get access token from ' + issuer)
        provider = OAuth2Session()
        response = provider.refresh_token(tokenUrl, refreshToken, **extra)
    except:
        print('Failed to get access token')
        raise SystemExit(1)
    return response["access_token"]
