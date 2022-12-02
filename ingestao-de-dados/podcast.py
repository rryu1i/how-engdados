#%%
import requests
from bs4 import BeautifulSoup as bs
import logging
import pandas as pd
import os
import re
import string


url = 'https://portalcafebrasil.com.br/todos/podcasts/page/{}?ajax=true'
directory = os.getcwd()


log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)


def get_podcasts(url):
    r = requests.get(url)
    soup = bs(r.text)
    return soup.find_all('h5')


def extract_podcasts(url):
    i = 1
    lst_podcast = []
    lst_get = get_podcasts(url.format(i))
    log.debug(f"Coletado {len(lst_get)} episódios do link: {url.format(i)}")
    while len(lst_get) > 0:
        lst_podcast = lst_podcast + lst_get
        i += 1
        lst_get = get_podcasts(url.format(i))
        log.debug(f"Coletado {len(lst_get)} episódios do link: {url.format(i)}")
    return lst_podcast


def create_df(lst_podcast):
    df = pd.DataFrame(columns=['nome', 'link'])
    for item in lst_podcast:
        df.loc[df.shape[0]] = [item.text, item.a['href']]
    return df


def saving_podcasts(df):
    df.to_csv('banco_de_podcastss.csv', sep=';', index=False)


def main():
    lst_podcast = extract_podcasts(url)
    df_podcast = create_df(lst_podcast)
    saving_podcasts(df_podcast)


if __name__ == '__main__':
    main()