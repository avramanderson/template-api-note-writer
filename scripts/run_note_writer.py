#!/usr/bin/env python3
import os
import sys
from requests_oauthlib import OAuth1Session

def main():
    api_key = os.getenv("X_API_KEY")
    api_secret = os.getenv("X_API_KEY_SECRET")
    access_token = os.getenv("X_ACCESS_TOKEN")
    access_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

    if not all([api_key, api_secret, access_token, access_secret]):
        print("Missing one or more secrets")
        sys.exit(2)

    oauth = OAuth1Session(
        api_key,
        client_secret=api_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_secret,
    )

    url = "https://api.twitter.com/1.1/account/verify_credentials.json"
    response = oauth.get(url)

    print("Status code:", response.status_code)

    if response.status_code == 200:
        print("Authentication successful.")
        sys.exit(0)
    else:
        print("Authentication failed.")
        print(response.text)
        sys.exit(1)

if __name__ == "__main__":
    main()
