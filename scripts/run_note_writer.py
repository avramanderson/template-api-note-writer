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

    # Community Notes v2 endpoint per X docs
    url = "https://api.x.com/2/notes/search/posts_eligible_for_notes"
    params = {
        "test_mode": "true",
        "max_results": "1",
        "tweet.fields": "author_id,created_at,referenced_tweets,media_metadata,note_tweet",
        "expansions": "attachments.media_keys,referenced_tweets.id,referenced_tweets.id.attachments.media_keys",
        "media.fields": "alt_text,duration_ms,height,media_key,preview_image_url,public_metrics,type,url,width,variants",
    }

    try:
        resp = oauth.get(
            url,
            params=params,
            headers={"User-Agent": "community-notes-note-writer/0.1"},
            timeout=30,
        )
        print("HTTP status:", resp.status_code)
        print("Response (first 800 chars):", resp.text[:800])

        # If you’re not enrolled as an AI Note Writer, this may return a JSON 403.
        if resp.status_code == 200:
            print("COMMUNITY_NOTES_API_OK")
            sys.exit(0)
        else:
            print("COMMUNITY_NOTES_API_NOT_OK")
            sys.exit(1)

    except Exception as e:
        print("ERROR:", type(e).__name__, str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
