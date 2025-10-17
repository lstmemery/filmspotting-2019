import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv


def get_api_key() -> str:
    """Retrieve the Challonge API key."""
    load_dotenv()
    return os.getenv('CHALLONGE_API')


def get_challonge_predictions(tournament: str, api_key: str) -> requests.Response:
    """Retrieve tournament predictions from Challonge API."""
    return requests.get(
        f'https://api.challonge.com/v1/tournaments/{tournament}/matches.json',
        params={
            'api_key': api_key,
            'include_predictions': 1
        }
    )


def process_predictions(response: requests.Response, output_path: Path) -> None:
    """Process and save prediction data."""
    matches = response.json()
    predictions = []

    for match in matches:
        match_id = match['match']['id']
        predictions_data = match['match'].get('predictions', [])
        for pred in predictions_data:
            predictions.append({
                'match_id': match_id,
                'user_id': pred['user_id'],
                'winner_id': pred['winner_id']
            })

    with open(output_path, 'w') as f:
        json.dump(predictions, f, indent=2)


if __name__ == '__main__':
    api_key = get_api_key()
    output_path = Path('../../data/madness2025_predictions.json')

    response = get_challonge_predictions('14453024', api_key)
    if response.status_code == 200:
        process_predictions(response, output_path)
        print(f"Predictions saved to {output_path}")
    else:
        print(f"Error: {response.status_code}")