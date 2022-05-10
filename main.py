import pandas as pd
import streamlit
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import backend as be
import utils as utils


with st.container():
    be.plot_intro_plot()

st.title('Try it yourself!')
st.subheader('In this section you can explore the complete dataset using our dashboard.')

with st.expander("Webpage parameters", expanded=True):
    colx, coly = st.columns([1, 1])

    with colx:
        years = list(range(1990, be.df.year.max()+1))
        st.write("The year selection decides the reference year")
        year_selected = st.selectbox('Year:', years, index=len(years)-1)

    with coly:
        st.write("The window size tells the dashboard how many years to look back to.")
        window_size = list(range(1, 21))
        window_size = st.selectbox('Window size:', window_size, index=19)


#plotting the scatter plot model
with st.container():
    st.subheader("Scatter Plot")
    st.write("Scatter plots are great to visualize relationships. In this section you have the possibility to build custom scatterplots from our data, then visualize the yearly changes.")

    col1, col2, col3 = st.columns([1, 1, 3])

    with col1:
        utils.add_empty_lines(6)
        x_selected = st.selectbox('x-axis:', list(be.df.columns)[3:], index=49)
        y_selected = st.selectbox('y-axis:', list(be.df.columns)[3:], index=126)
    with col2:
        utils.add_empty_lines(6)
        size_selected = st.selectbox('size:', ['population', 'gdp'], index=0)
        color_selected = st.selectbox('color by:', ['continent', 'country'], index=0)
    with col3:
        hover = '%{country}<br>X: %{x:.2f} <br>Y: %{y:.2f}'
        be.create_scatter_plot(x=x_selected, y=y_selected, color=color_selected, size=size_selected, year_min=year_selected-window_size, hover=hover)


#plotting the choropleth model
with st.container():
    st.subheader("Choropleth and Line Plots")
    st.write("Choropleth plots are great to visualize data on maps. In this section you can choose any of the parameters of the dataset and visualize the change across the years. To further aid your understanding, you can select various countries to compare using the line charts.")
    col1, col2 = st.columns([2,2])
    with col1:
        y_map = st.selectbox('color-map:', list(be.df.columns)[3:], index=4)
    with col2:
        countries_selected = st.multiselect('select country', list(be.df['country'].unique()), default=['World'])


    col2, col3 = st.columns([2, 2])

    with col2:
        hover = '%{country}<br>X: %{x:.2f} <br>Y: %{y:.2f}'
        be.choropleth_plot(y=y_map, year_min=year_selected-window_size)

    with col3:
        be.create_line_plot(y=y_map, year_min=year_selected-window_size, country_filt=countries_selected)



#plotting tree-maps
with st.container():
    st.subheader("Treemap Charts")
    c1, c2 = st.columns([1,2])

    with c1:
        st.write("In this section you will be able to visualize the data using treemaps. Treemap charts visualize hierarchical data using nested rectangles. To control the size and color of the rectangles, please tune the parameters below. We have also decoupled the year parameter for this chart.")
        box_size = st.selectbox('tree-size:', list(be.df.columns)[3:], index=49)
        box_color = st.selectbox('tree-color:', list(be.df.columns)[3:], index=127)
        year_box = st.selectbox('tree-year:', list(range(2010, 2019)), index=8)
    with c2:
        be.create_tree_plot(box_color, box_size, year_box)



#
# with st.container():
#     col_p1, col_p2, col_p3 = st.columns([2, 2, 2])
#
#     with col_p1:
#         be.create_scatter_plot(x=x_selected, y=y_selected, hover=None)
#
#     with col_p2:
#         be.choropleth_plot(y=y_selected)
#
#     with col_p3:
#         be.create_line_plot(y=y_selected, country_filt=['World'])
#
#
#     col_p1, col_p2, col_p3 = st.columns([2, 2, 2])
#
#     # with col_p1:
#     # be.create_paris_agreement_nations()
#     # create_line_plot2(df_co2)
#
#     with col_p2:
#         be.create_tree_plot(x='fossil_share_energy', y='co2_per_capita')
#
#     with col_p3:
#         be.create_lineplot_change(y=y_selected, current_year=2018, window_size=10)
#
#
#
#     col_t1, col_t2, col_t3 = st.columns([2, 2, 2])
#
#     with col_t1:
#         be.create_emission_pie()
#
#     with col_t2:
#         hover = '<b>%{label} </b> <br>Fossil Energy: %{color:.2f}% <br>CO2 per capita: %{value:.2f}'
#         be.create_tree_plot_window('fossil_share_energy', 'co2_per_capita', 2018, 10, hover)
#
#     with col_t3:
#         hover = '<b>%{label} </b> <br>Renewables Share Change: %{color:.2f}% <br>CO2 per capita: %{value:.2f}'
#         be.create_tree_plot_window('renewables_share_energy', 'co2_per_capita', 2018, 10, reverse=True, hover=hover)
#
#     # col_t1, col_t2= st.columns([2,2])
#
#     with st.container():
#         be.create_energy_consumption_source()
#
#     # with col_t2:
#     #     hover = '<b>%{label} </b> <br>Fossil Energy: %{color:.2f}% <br>CO2 per capita: %{value:.2f}'
#     #     be.create_tree_plot_window('fossil_share_energy', 'co2_per_capita', 2018, 10, hover)
#     #
#     # with col_t3:
#     #     hover = '<b>%{label} </b> <br>Renewables Share Change: %{color:.2f}% <br>CO2 per capita: %{value:.2f}'
#     #     be.create_tree_plot_window('renewables_share_energy', 'co2_per_capita', 2018, 10, reverse=True, hover=hover)
#
#
#     # with col_p3:
#     #     create_line_plot(df_co2, y=y_selected, country_filt=countries_selected)
#     """
#     Speaking about roller coaster rides… The Friends viewers have also been on a bit of a ride.
#     The episode with the lowest overall sentiment was Episode 1 in Season 4: _The one with the Jellyfish_, as you probably remember.
#     The crazy thing is that in the same season we have one of the highest sentiment scores of an episode - Episode 5: _The one with Joey's new girlfriend_.
#     """
