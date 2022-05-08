import pandas as pd
import streamlit
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import backend as be
import utils as utils

st.set_page_config(page_title="SocialData2022",layout='wide')

st.title('Welcome to the project website for the course Social graphs and interactions (02805)')
st.subheader('Made by Adrienne, Usama, and Ferenc')


with st.container():


    colx, coly, col2, col3 = st.columns([1, 1, 2, 2])

    with colx:
        x_selected = st.selectbox('x-axis:', list(be.df.columns), index=3)

    with coly:
        y_selected = st.selectbox('y-axis:', list(be.df.columns), index=4)

    with col2:
        col2.header('Geo-Scatterplot')

    with col3:
        defaults = be.df[['country', 'year', y_selected]].dropna()
        max_year = defaults['year'].max()
        defaults = defaults[defaults['year'] == max_year].sort_values(y_selected, ascending=False).head(7)
        defaults = list(defaults['country'].values) + ['World']
        countries_selected = st.multiselect('select country', list(be.df['country'].unique()), default=defaults)

    col_p1, col_p2, col_p3 = st.columns([2, 2, 2])

    with col_p1:
        be.create_scatter_plot(x=x_selected, y=y_selected)

    with col_p2:
        be.choropleth_plot(y=y_selected)

    with col_p3:
        be.create_line_plot(y=y_selected, country_filt=countries_selected)


    col_p1, col_p2, col_p3 = st.columns([2, 2, 2])

    with col_p1:
        be.create_paris_agreement_nations()
        # create_line_plot2(df_co2)

    with col_p2:
        be.create_tree_plot(x='fossil_share_energy', y='co2_per_capita')

    with col_p3:
        be.create_lineplot_change(y=y_selected, current_year=2018, window_size=10)



    col_t1, col_t2, col_t3 = st.columns([2, 2, 2])

    with col_t1:
        be.create_emission_pie()

    with col_t2:
        hover = '<b>%{label} </b> <br>Fossil Energy: %{color:.2f}% <br>CO2 per capita: %{value:.2f}'
        be.create_tree_plot_window('fossil_share_energy', 'co2_per_capita', 2018, 10, hover)

    with col_t3:
        hover = '<b>%{label} </b> <br>Renewables Share Change: %{color:.2f}% <br>CO2 per capita: %{value:.2f}'
        be.create_tree_plot_window('renewables_share_energy', 'co2_per_capita', 2018, 10, reverse=True, hover=hover)


    # with col_p3:
    #     create_line_plot(df_co2, y=y_selected, country_filt=countries_selected)
    """
    Speaking about roller coaster rides… The Friends viewers have also been on a bit of a ride.
    The episode with the lowest overall sentiment was Episode 1 in Season 4: _The one with the Jellyfish_, as you probably remember.
    The crazy thing is that in the same season we have one of the highest sentiment scores of an episode - Episode 5: _The one with Joey's new girlfriend_.
    """


