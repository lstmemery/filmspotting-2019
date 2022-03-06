import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv


def get_api_key() -> str:
    """Retrieve the Challonge API key."""
    load_dotenv()
    return os.getenv('CHALLONGE_API')


def get_challonge_api_info(tournament: str, api_key: str) -> requests.Response:
    """Retrieve all JSON tournament information from Challonge."""
    return requests.get(
        f'https://api.challonge.com/v1/tournaments/{tournament}.json',
        params={
            'api_key': api_key,
            'include_participants': 1,
            'include_matches': 1,
        },
    )


if __name__ == '__main__':
    load_dotenv()
    api_key = get_api_key()
    challonge_response = get_challonge_api_info('madness2022', api_key)

    with open(Path('../../data/madness2022.json'), 'w+') as file_path:
        json.dump(challonge_response.json(), file_path, indent=2)
