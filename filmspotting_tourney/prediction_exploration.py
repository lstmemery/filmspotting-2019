import ast
import json
import re
from glob import glob

import pandas as pd

from bs4 import BeautifulSoup

def prediction_script(tag):
    return tag.has_attr('data-react-class')

def dfify(filename):
    with open(filename) as check_file:
        soup = BeautifulSoup(check_file.read())
        prediction = soup.find(prediction_script)
        props = prediction.attrs['data-react-props']
        predictions = json.loads(props)['initialPrediction']['data']
        return pd.DataFrame(predictions, columns=['Match', '?', 'Winner'])

predictions = glob('../data/predictions/*.html')

all_dfs = [dfify(prediction) for prediction in predictions]
super_df = pd.concat(all_dfs)

super_df.to_csv('../data/all_preds2021.csv', index=False)