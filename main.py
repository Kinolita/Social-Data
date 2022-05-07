import pandas as pd
import streamlit
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import utils as utils
import backend as backend
#from backend import *
#from utils import *

df_co2, df_en, df_temp = utils.data_loader()
LABELS = utils.label_loader()
df = pd.merge(df_en, df_co2.drop(['gdp', 'population', 'continent', 'country'], axis=1), on=['iso_code', 'year'])
st.set_page_config(page_title="SocialData2022",layout='wide')


st.title('Welcome to the project website for the course Social graphs and interactions (02805)')
st.subheader('Made by Adrienne, Usama, and Ferenc')


with st.container():


    colx, coly, col2, col3 = st.columns([1, 1, 2, 2])

    with colx:
        x_selected = st.selectbox('x-axis:', list(df.columns), index=3)

    with coly:
        y_selected = st.selectbox('y-axis:', list(df.columns), index=4)

    with col2:
        col2.header('Geo-Scatterplot')

    with col3:
        defaults = df[['country', 'year', y_selected]].dropna()
        max_year = defaults['year'].max()
        defaults = defaults[defaults['year'] == max_year].sort_values(y_selected, ascending=False).head(7)
        defaults = list(defaults['country'].values) + ['World']
        countries_selected = st.multiselect('select country', list(df['country'].unique()), default=defaults)

    col_p1, col_p2, col_p3 = st.columns([2, 2, 2])

    with col_p1:
        backend.create_scatter_plot(df, x=x_selected, y=y_selected)

    with col_p2:
        backend.choropleth_plot(df, y=y_selected)

    with col_p3:
        backend.create_line_plot(df, y=y_selected, country_filt=countries_selected)


    col_p1, col_p2, col_p3 = st.columns([2, 2, 2])

    with col_p1:
        backend.create_line_plot2(df_co2)

    with col_p2:
        backend.create_tree_plot(df, x=x_selected, y=y_selected)







    # with col_p2:
    #     backend.create_scattermap_plot(df_co2, y=y_selected)

    # with col_p3:
    #     backend.create_line_plot(df_co2, y=y_selected, country_filt=countries_selected)
    """
    Speaking about roller coaster rides… The Friends viewers have also been on a bit of a ride.
    The episode with the lowest overall sentiment was Episode 1 in Season 4: _The one with the Jellyfish_, as you probably remember.
    The crazy thing is that in the same season we have one of the highest sentiment scores of an episode - Episode 5: _The one with Joey's new girlfriend_.
    """


