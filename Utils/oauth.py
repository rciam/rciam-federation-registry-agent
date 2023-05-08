from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

"""Refreshing an OAuth 2 token using a refresh token.
:param issuer: The token endpoint, must be HTTPS.
:param refresh_token: The refresh_token to use.
:param client_id: Client id obtained during registration
:param client_secret: Client secret obtained during registration
:return: An access token
"""


def refresh_token_grant(issuer, refresh_token, client_id, client_secret):
    token_url = issuer + "/token"

    extra = {"client_id": client_id, "client_secret": client_secret}

    try:
        print("Get access token from " + issuer)
        provider = OAuth2Session()
        response = provider.refresh_token(token_url, refresh_token, **extra)
    except:
        print("Failed to get access token")
        raise SystemExit(1)
    return response["access_token"]


def client_credentials_grant(issuer, client_id, client_secret):
    token_url = issuer + "/protocol/openid-connect/token"

    try:
        print("[client_credentials_grant] Get access token from " + issuer)
        client = BackendApplicationClient(client_id=client_id)
        oauth = OAuth2Session(client=client)
        response = oauth.fetch_token(token_url=token_url, client_id=client_id, client_secret=client_secret)
        print("[client_credentials_grant] Access Token: " + response["access_token"])
    except:
        print("[client_credentials_grant] Failed to get access token")
        raise SystemExit(1)
    return response["access_token"]
