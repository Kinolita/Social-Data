import numpy as np
import pandas as pd
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import streamlit as st

PATH = Path(__file__).resolve().parents[0] / 'data'

def get_continent(iso, countries):
    if iso in countries.index.to_list():
        return countries.loc[iso, 'region']
    else:
        return np.nan

def get_label(df, label):
    return df.loc[label, 'description'].split('.')[0]

@st.cache
def data_loader():
    df_energy = pd.read_csv('https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv')
    df_co2 = pd.read_csv('https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv')
    df_temp = pd.read_csv(PATH / 'temperature-anomaly.csv')
    df_countries = pd.read_csv(PATH / 'continents2.csv', index_col=2)
    df_energy['continent'] = df_energy['iso_code'].apply(lambda x: get_continent(x, df_countries))
    df_co2['continent'] = df_co2['iso_code'].apply(lambda x: get_continent(x, df_countries))
    df_energy_dist = pd.read_csv(PATH / 'energy_distribution.csv')
    df = pd.merge(df_energy, df_co2.drop(['gdp', 'population', 'continent', 'country'], axis=1), on=['iso_code', 'year'])

    return df, df_temp, df_energy_dist

def label_loader():
    df_energy_labels = pd.read_csv('https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-codebook.csv', index_col=0)
    df_co2_labels = pd.read_csv('https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-codebook.csv', index_col=0)
    labels = pd.concat([df_energy_labels, df_co2_labels]).reset_index().drop_duplicates('column')
    return labels.set_index('column')






def get_current_members():

    url = 'https://en.wikipedia.org/wiki/List_of_parties_to_the_Paris_Agreement'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    table1 = soup.find("table", id="wikitable sortable")
    print(table1)
    data = []
    for i in table1.find_all('td'):
        title = i.text
        data.append(title)

    headers = data[:3]
    new_data = pd.DataFrame(columns = headers)

    for j in table1.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        length = len(new_data)
        new_data.loc[length] = row

    # new_data['Signature'] = [2016 for date in new_data['Signature']]
    # new_data.rename(columns = {"Ratification, Acceptance(A), Approval(AA), Accession(a)": "Accepted", "Participant": "Country", "Signature": "Signed"}, inplace=True)
    # new_data['Accepted'] = [date.strip().split(" ")[2] if len(date) > 1 else 2016 for date in new_data['Accepted']]
    return new_data