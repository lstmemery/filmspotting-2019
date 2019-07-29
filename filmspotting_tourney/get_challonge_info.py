import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv


def get_api_key():
    load_dotenv()
    return os.getenv("CHALLONGE_API")


def get_challonge_api_info(tournament, api_key):
    return requests.get(f"https://api.challonge.com/v1/tournaments/{tournament}.json",
                        params={'api_key': api_key,
                                'include_participants': 1,
                                'include_matches': 1
                                })


if __name__ == '__main__':
    api_key = get_api_key()
    results = get_challonge_api_info('madness19', api_key)

    with open(Path("../data/madness19-post.json"), 'w+') as file_path:
        json.dump(results.json(), file_path, indent=2)
