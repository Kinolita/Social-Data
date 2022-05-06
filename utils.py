import numpy as np
import pandas as pd
from pathlib import Path

PATH = Path(__file__).resolve().parents[0] / 'data'
CONTINENTS = ['World', 'Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania', 'Antarctica']

def get_continent(iso, countries):
    if iso in countries.index.to_list():
        return countries.loc[iso, 'region']
    else:
        return np.nan

def get_label(df, label):
    return df.loc[label, 'description'].split('.')[0]

def data_loader():
    df_energy = pd.read_csv('https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv')
    df_co2 = pd.read_csv('https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv')
    df_temp = pd.read_csv(PATH / 'temperature-anomaly.csv')
    df_countries = pd.read_csv(PATH / 'continents2.csv', index_col=2)
    df_energy['continent'] = df_energy['iso_code'].apply(lambda x: get_continent(x, df_countries))
    df_co2['continent'] = df_co2['iso_code'].apply(lambda x: get_continent(x, df_countries))

    return df_co2, df_energy, df_temp

def label_loader():
    df_energy_labels = pd.read_csv('https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-codebook.csv', index_col=0)
    df_co2_labels = pd.read_csv('https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-codebook.csv', index_col=0)
    labels = pd.concat([df_energy_labels, df_co2_labels])
    return labels.drop_duplicates()