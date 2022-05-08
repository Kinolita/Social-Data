import numpy as np
import pandas as pd
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import streamlit as st

PATH = Path(__file__).resolve().parents[0] / 'data'

def add_empty_lines(nr_lines):
    for i in range(nr_lines):
        st.write("")

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




def fix_values(string):
    try:
        return float(string.split('%')[0])
    except Exception as e:
        return np.nan

def get_current_member_countries():

    url = 'https://en.wikipedia.org/wiki/List_of_parties_to_the_Paris_Agreement'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')

    table1 = soup.find("table", {"class": "wikitable"})
    df=pd.read_html(str(table1))
    df=pd.DataFrame(df[0])
    df.rename(columns = {"Party[12]": "Country", "Percentage of greenhousegases for ratification[5]": "Percentage of greenhousegases for ratification"}, inplace= True)
    df = df.iloc[:-1 , :]
    df['Date of signature'] = [str(x) for x in df['Date of signature']]
    df['Date of signature'] = [x.strip().split(" ") for x in df['Date of signature']]
    df['Date of signature'] = [x[2] if len(x) > 1 else 2016 for x in df['Date of signature']]
    df["Date of ratification, acceptance, approval, or accession"] = df['Date of ratification, acceptance, approval, or accession'].apply(lambda x: x.split(" ")[2][:4])
    df['Date of entry into force'] = df['Date of entry into force'].apply(lambda y: y.split(" ")[2][:4])
    df["Percentage of greenhousegases for ratification"] = df["Percentage of greenhousegases for ratification"].apply(lambda x: fix_values(x))
    return df