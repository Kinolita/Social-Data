import pandas as pd
import streamlit
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import backend as be
import utils as utils

st.set_page_config(page_title="Final Project • 02806",layout='wide')

st.markdown("<h1><center>Welcome to the project website for <br> Social Data Analysis and Visualization (02806)</center></h1>",
            unsafe_allow_html=True)

with st.container():
    n1, n2, n3 = st.columns(3)
    with n1:
        st.markdown("<h3><center> Adrienne Cohrt <br> s184426 </center></h3>", unsafe_allow_html=True)

    with n2:
        st.markdown("<h3><center> Ferenc Fodor <br> s220356 </center></h3>", unsafe_allow_html=True)

    with n3:
        st.markdown("<h3><center> Usama Mir <br> s134187 </center></h3>", unsafe_allow_html=True)

"""With the reduction of rainforests and the ozone layer and the increasingly drastic changes in our climate, the world found it important 
to create an international treaty in 2016 called the Paris Agreement. This agreement, which was adopted by 196 countries, aims to limit global 
warming by controlling and reducing greenhouse gas emissions as soon as possible. While the actions and progress of each country are not required to 
be transparent until 2024, low and zero-carbon solutions and carbon neutrality targets are becoming much more common. But while it appears that 
countries are making an effort to honor the agreements and work towards carbon neutrality, what is the actual progress to date?"""

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


with st.container():
    col_t1, col_t2 = st.columns([2,1])

    with col_t1:
        be.create_emission_pie()

    with col_t2:
        st.write("Here we can see the distribution of CO2 emissions in the world in 2016. The major contributors can be broken into three categories of impact: industry, buildings, and transport. Later on we will take a look at how these individual categories have progressed and where they stand today.")
    

with st.container():
    col_t1, col_t2 = st.columns([1, 2])
    x = 'fossil_share_energy'
    y = 'co2'
    with col_t1:
        """
        Of course some countries will be larger contributers of greenhouse gasses than others due to their industry level or population. 
        These countries will be under a natural spotlight to imporve as they will have the largest contribution to the reduction of 
        global warming but they should not be expected to carry the responsibility of this for the entire world. Every little bit helps. 
        Here we can see the amount of carbon dioxide emissions represented by sized boxes for each country and continent. 
        The color of each box indicates how much of those emissions are the result of fossil fuels.
        """
        st.write(f">Size of the box: {utils.get_label(be.LABELS, y)}")
        st.write(f">Coloring: {utils.get_label(be.LABELS, x)}")
    with col_t2:
        be.create_tree_plot(x=x, y=y)


    """
    SOo..... From here we could look at the 3 categories (if possible to make visualizations of that) and see how they go renewable% wise from 2016 onwards.

    """


    col2, col3 = st.columns(2)
    
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

