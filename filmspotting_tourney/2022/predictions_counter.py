import pprint
from collections import Counter, defaultdict
import json
from typing import Tuple, Dict


def parse_names(film_names):
    name_dict = {}
    first_round_matches = film_names.get('matches_by_round').get('1')
    for match in first_round_matches:
        name_dict[match.get('player1').get('id')] = match.get('player1').get('display_name')
        name_dict[match.get('player2').get('id')] = match.get('player2').get('display_name')

    return name_dict

def translate_names(match: str, name_dict: Dict) -> Tuple:
    split_names = match.strip().split(',')
    return int(split_names[0]), int(split_names[1]), name_dict[int(split_names[2])]


if __name__ == '__main__':
    with open('/home/deadhand/Documents/filmspotting-2019/data/tourney2022.json', 'r') as film_names_file:
        film_names = json.load(film_names_file)
        film_name_dict = parse_names(film_names)

    with open('/home/deadhand/Documents/filmspotting-2019/results/2022_predictions.csv', 'r') as file:
        predictions = {}
        for i in file.readlines()[1:]:
            match, position, winner = translate_names(i, film_name_dict)
            if match not in predictions:
                predictions[match] = Counter()
            predictions[match][winner] += 1



        pprint.pprint(predictions)


        # prediction_counter = [Counter(translate_names(i, film_name_dict)) for i in file.readlines()[1:]]


    # pprint.pprint(prediction_counter.most_common(100))