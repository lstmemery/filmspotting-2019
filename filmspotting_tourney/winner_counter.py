from collections import Counter
from glob import glob

from bs4 import BeautifulSoup

predictions = glob('../data/predictions/*.html')

def winner(filename):
    with open(filename) as check_file:
        soup = BeautifulSoup(check_file.read())
        return soup.find_all(attrs={'class': 'container-fluid -with-content-gutters'})[1].get_text().split('\n')[-2]

print(Counter(winner(i) for i in predictions))
