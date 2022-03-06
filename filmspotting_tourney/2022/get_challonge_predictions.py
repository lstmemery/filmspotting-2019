import asyncio
import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv
import challonge


def get_api_key() -> str:
    """Retrieve the Challonge API key."""
    load_dotenv()
    return os.getenv('CHALLONGE_API')


def get_challonge_api_info(tournament: str, api_key: str) -> requests.Response:
    """Retrieve all JSON tournament information from Challonge."""
    return requests.get(
        f'https://lstmemery:{api_key}@api.challonge.com/v1/tournaments/{tournament}.json',
        params={
            'api_key': api_key,
            'include_participants': 1,
            'include_matches': 1,
            # 'include_predictions': 1
        },
    )

async def get_predictions(loop):
    load_dotenv()
    api_key = get_api_key()
    challonge.set_credentials('lstmemery', api_key)

    tourney = await challonge.tournaments.show('madness2022', **{            'include_participants': 1,
            'include_matches': 1,
            'include_predictions': 1})
    print('Done')


def get_predictions_thread():
    load_dotenv()
    api_key = get_api_key()
    challonge.set_credentials('lstmemery', api_key)

    return challonge.tournaments.show('madness2022', **{'include_participants': 1,
            'include_matches': 1,
            'include_predictions': 1})

if __name__ == '__main__':
    get_predictions_thread()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(get_predictions(loop))
    # print('Done')

# if __name__ == '__main__':
#     tourney = get_predictions()
#     print(tourney)
    #
    # api_key = get_api_key()
    # challonge_response = get_challonge_api_info('madness2021', api_key)
    #
    # with open(Path('../data/madness21.json'), 'w+') as file_path:
    #     json.dump(challonge_response.json(), file_path, indent=2)
