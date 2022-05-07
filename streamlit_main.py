import pandas as pd
import streamlit
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import backend as be
import utils as utils


st.title('Welcome to the project website for the course Social graphs and interactions (02805)')
st.subheader('Made by Adrienne, Usama, and Ferenc')

st.write('With the reduction of rainforests and the ozone layer and the increasingly drastic changes in our climate, the world found it important to create an international treaty in 2016 called the Paris Agreement. This agreement, which was adopted by 196 countries, aims to limit global warming by controlling and reducing greenhouse gas emissions as soon as possible. While the actions and progress of each country are not required to be transparent until 2024, low and zero-carbon solutions and carbon neutrality targets are becoming much more common. But while it appears that countries are making an effort to honor the agreements and work towards carbon neutrality, what is the actual progress to date?')
st.write("Visulization or table here for the countries? idk")

with st.expander("Webpage parameters", expanded=True):
    colx, coly, col2, col3 = st.columns([1, 1, 2, 2])

    with colx:
        years = list(range(2000, be.df.year.max()))
        year_selected = st.selectbox('Year:', years, index=len(years)-1)

    with coly:
        window_size = list(range(1, 11))
        window_size = st.selectbox('Window size:', window_size, index=4)

    with col2:
        x_selected = st.selectbox('x-axis:', list(be.df.columns), index=3)

    with col3:
        y_selected = st.selectbox('y-axis:', list(be.df.columns), index=4)

st.write("##")

st.write("Below we take a look at the distribution of co2 emissions as it was in 2016. Emissions can be broken into three major categories of impact: industry, buildings, and transport.")
with st.container():
    col_t1, col_t2 = st.columns([2, 1])

    with col_t1:
        be.create_emission_pie()

    with col_t2:
        st.write("> Source of CO2 emissions in %")


with st.container():
    col_t1, col_t2 = st.columns([1, 2])
    x = 'fossil_share_energy'
    y = 'co2'
    with col_t1:
        st.write(f">Size of the box: {utils.get_label(be.LABELS, y)}")
        st.write(f">Coloring: {utils.get_label(be.LABELS, x)}")
    with col_t2:
        be.create_tree_plot(x=x, y=y)





    col2, col3 = st.columns(2)
    #
    with col2:
        col2.header('Geo-Scatterplot')

    with col3:
        countries_selected = st.multiselect('select country', list(be.df['country'].unique()), default=['World'])

    col_p1, col_p2, col_p3 = st.columns(3)

    with col_p1:
        be.create_scatter_plot(x=x_selected, y=y_selected)

    with col_p2:
        be.choropleth_plot(y=y_selected)

    with col_p3:
        be.create_line_plot(y=y_selected, country_filt=countries_selected)


    col_p1, col_p2, col_p3 = st.columns(3)

    with col_p1:
        pass
    #     be.create_line_plot2(df_co2)

    with col_p2:
        pass
    with col_p3:
        be.create_lineplot_change(y=y_selected, current_year=2020, window_size=10)





    # with col_p2:
    #     create_scattermap_plot(df_co2, y=y_selected)

    # with col_p3:
    #     create_line_plot(df_co2, y=y_selected, country_filt=countries_selected)
    """
    Speaking about roller coaster rides… The Friends viewers have also been on a bit of a ride.
    The episode with the lowest overall sentiment was Episode 1 in Season 4: _The one with the Jellyfish_, as you probably remember.
    The crazy thing is that in the same season we have one of the highest sentiment scores of an episode - Episode 5: _The one with Joey's new girlfriend_.
    """


