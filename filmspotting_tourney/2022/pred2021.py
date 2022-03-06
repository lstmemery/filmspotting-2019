import json

import pandas as pd

df = pd.read_csv('../data/all_preds2021.csv')
df_count = df.groupby(['Match', 'Winner']).count().reset_index()

def get_film_names():
    with open('../data/madness2021.json') as madness_file:
        madness = json.load(madness_file)
        par_dict = {}
        for par in madness['tournament']['participants']:
            par_dict[par['participant']['id']] = par['participant']['name']
    return par_dict

par_dict = get_film_names()
df_count['name'] = df_count['Winner'].apply(lambda x: par_dict[x])
df_count.to_csv('../data/2021_counts.csv', index=False)