#!/usr/bin/env python3

import os
import sys
from requests_oauthlib import OAuth1Session

def main():
    print("Starting Community Notes API test...")

    # Load secrets from environment
    api_key = os.getenv("X_API_KEY")
    api_secret = os.getenv("X_API_KEY_SECRET")
    access_token = os.getenv("X_ACCESS_TOKEN")
    access_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

    if not all([api_key, api_secret, access_token, access_secret]):
        print("ERROR: Missing one or more secrets.")
        sys.exit(2)

    # Create OAuth1 session
    oauth = OAuth1Session(
        api_key,
        client_secret=api_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_secret,
    )

    # Community Notes endpoint (correct base URL)
    url = "https://api.x.com/2/notes/search/posts_eligible_for_notes"
    params = {
        "test_mode": "true",
        "max_results": "1"
    }

    try:
        response = oauth.get(url, params=params, timeout=30)

        print("HTTP Status:", response.status_code)
        print("Response (first 800 chars):")
        print(response.text[:800])

        if response.status_code == 200:
            print("SUCCESS: Community Notes endpoint reachable.")
            sys.exit(0)
        else:
            print("Request did not return 200.")
            sys.exit(1)

    except Exception as e:
        print("EXCEPTION:", str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
