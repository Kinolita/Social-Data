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


data1 = "https://github.com/owid/energy-data"
data2 = "https://github.com/owid/co2-data"
rep = "https://github.com/Kinolita/Social-Data"
nb = "https://github.com/Kinolita/Social-Data/blob/main/helper_notebook.ipynb"
st.write("Source 1: [Data on Energy by our World in Data](%s)" % data1)
st.write("Source 2: [Data on CO2 and greenhouse gas emissions by Our World in Data](%s)" % data2)
st.write("Links to our [repository](%s) and our [explainer notebook](%s)." % (rep, nb))


"""
With the reduction of rainforests and the ozone layer and the increasingly drastic changes in our climate, the world found it important 
to create an international treaty in 2016 called the Paris Agreement. This agreement, which was adopted by 196 countries, aims to limit global 
warming by controlling and reducing greenhouse gas emissions as soon as possible. While the actions and progress of each country are not required to 
be transparent until 2024, low and zero-carbon solutions and carbon neutrality targets are becoming much more common. But while it appears that 
countries are making an effort to honor the agreements and work towards carbon neutrality, what is the actual progress to date?
"""

"""
Below on the left, we can see the average change in temperature of the earth over the last two centuries and how it has risen consistently and significantly since 1980. 
On the right we see a display of global CO2 emissions since 1900 by continent. 
It is interesting to note that the rise in emissions coincides with the rise in global temperatures.
"""

be.plot_intro_plot()

"""
In Europe and specifically Denmark we hear a lot about climate changes and how we as countries should
strive towards drastically lowering our CO2 emissions. While there is a general concensus in the population -
at least in Denmark - that this is a huge issue, we often are led to believe something else by our politicians.
It can be very hard to fact check what politicians, global companies etc. are saying in regards to the climate,
since their statements are often biased by their subjective goals. Because of that, this article will help
create transparency towards how the actual situation and development have been in regards to lowering CO2 emissions
and how far have we come. We provide the facts, but its up to you to interpret them!"""

with st.container():
    col_t1, col_t2 = st.columns([2,1])

    with col_t1:
        be.create_emission_pie()

    with col_t2:
        utils.add_empty_lines(8)
        """
        Here we can see the distribution of CO2 emissions in the world in 2016. 
        The major source of greenhouse gasses is clearly in the energy sector with the main contributers of this being: industry, buildings, and transport.
        You can try and click around to see what the different sectors consist of.
        """    

with st.container():
    col_t1, col_t2 = st.columns([1, 2])
    x = 'fossil_share_energy'
    y = 'co2'
    with col_t1:
        utils.add_empty_lines(4)

        """
        If we take a look at the same emissions per country, we can see which ones are the largest contributers to this. 
        Of course some countries will be larger contributers than others simply due to their industry levels or population. 
        These countries will be under a natural spotlight to improve as they could also have the largest contribution to the reduction of 
        global warming. This being said, they should not be expected to carry the responsibility of this for the entire world. Every little bit helps. 

        Here we can see the amount of carbon dioxide emissions represented by sized boxes for each country and continent. 
        The color of each box indicates how much of those emissions are the result of fossil fuels.
        """
        # st.write(f">Size of the box: {utils.get_label(be.LABELS, y)}")
        # st.write(f">Coloring: {utils.get_label(be.LABELS, x)}")

    with col_t2:
        be.create_tree_plot(x=x, y=y)

with st.container():
    col2, col3 = st.columns(2)

    with col2:
        be.create_tree_plot(x=x, y="co2_per_capita")
    with col3:
        utils.add_empty_lines(8)
        """
        If we take this same data and equalize the box sizes to emissions per capita we see a much different story 
        where countries that don't necessarily have a large impact globally have a very large impact per citizen. 

        It's important to keep this distinction in mind as it can be very relevant. 
        Many politicians can be shown conflicting or misleading data which is then filtered out to the masses.
        """

with st.container():
    col2, col3 = st.columns(2)

    with col2:
        utils.add_empty_lines(8)
        """
        In this graph we can see the general trend of all the countries of the world in regards to their production 
        of CO2 in tonnes per person. The world is highlighted, and while there have been both improvements and unimprovements in various countries,
        it's clear to see that the general trend so far has not changed. This tells us that while countries may be beginning to implement their 
        low and zero-carbon solutions we still have a long way to go before we see the fruits of our labor.
        """
    with col3:
        be.create_lineplot_change(y="co2_per_capita", current_year=2020, window_size=10)

with st.container():
    col2, col3 = st.columns(2)

    with col2:
        be.create_energy_consumption_source()

    with col3:
        utils.add_empty_lines(8)

        """
        In this graph we can see how much each energy type consists of the yearly production in relation to each other. 
        For instance its easy to spot that coal and oil are by far the biggest contributers to energy consumption. 
        The years are at the x-axis while the y-axis represents the energy in Terawatt per hours.
        """

#Dashboard
st.subheader('Try it yourself!')

"""
At this point we have given a brief but thorough introduction to some of the data that can be found on CO2 emissions,
energy consumption, and the paris agreement in general. As we started by saying: We will only provide the data, its up to
you to evaluate and interpret the numbers. Since we have shown some plots its now time for you to "play" with the data yourself. 
In the following section we have made some generic graphs where you will have the opporunity to change the variables for the
plots to examine the data yourself. Maybe you will find something interesting!
"""


with st.expander("Webpage parameters", expanded=True):
    colx, coly = st.columns([1, 1])

    with colx:
        years = list(range(1990, be.df.year.max()+1))
        st.write("The year selection decides the reference year")
        year_selected = st.selectbox('Year:', years, index=len(years)-1)

    with coly:
        st.write(
            "The window size indicates how many years into the past to visualize.")
        window_size = list(range(1, 21))
        window_size = st.selectbox('Window size:', window_size, index=19)


#plotting the scatter plot model
with st.container():
    st.subheader("Scatter Plot")
    st.write("Scatter plots are great to visualize relationships. Here you have the possibility to build custom scatterplots from our data, then visualize the yearly changes.")

    col1, col2, col3 = st.columns([1, 1, 3])

    with col1:
        utils.add_empty_lines(6)
        x_selected = st.selectbox('X-axis:', list(be.df.columns)[3:], index=49)
        y_selected = st.selectbox(
            'Y-axis:', list(be.df.columns)[3:], index=126)
    with col2:
        utils.add_empty_lines(6)
        size_selected = st.selectbox('Circle size:', ['population', 'gdp'], index=0)
        color_selected = st.selectbox(
            'Color by:', ['continent', 'country'], index=0)
    with col3:
        hover = '%{country}<br>X: %{x:.2f} <br>Y: %{y:.2f}'
        be.create_scatter_plot(x=x_selected, y=y_selected, color=color_selected,
                               size=size_selected, year_min=year_selected-window_size, hover=hover)


#plotting the choropleth model
with st.container():
    st.subheader("Choropleth and Line Plots")
    st.write("Choropleth plots are a great way to visualize data on maps. In this section you can choose any of the parameters of the dataset and visualize the change across the years. To further aid your understanding, you can select various countries to compare using the line plot.")
    col1, col2 = st.columns([2, 2])
    with col1:
        y_map = st.selectbox('Select focus data for the map:', list(be.df.columns)[3:], index=4)
    with col2:
        countries_selected = st.multiselect('Select country(s) for the line plot', list(
            be.df['country'].unique()), default=['World'])

    col2, col3 = st.columns([2, 2])

    with col2:
        hover = '%{country}<br>X: %{x:.2f} <br>Y: %{y:.2f}'
        be.choropleth_plot(y=y_map, year_min=year_selected-window_size)

    with col3:
        be.create_line_plot(y=y_map, year_min=year_selected -
                            window_size, country_filt=countries_selected)


#plotting tree-maps
with st.container():
    st.subheader("Treemap Charts")
    c1, c2 = st.columns([1, 2])

    with c1:
        st.write("In this section you can visualize the data using treemaps. Treemap charts visualize hierarchical data using nested rectangles. To control the size and color of the rectangles tune the parameters below. We have also decoupled the year parameter for this chart.")
        box_size = st.selectbox(
            'Box size:', list(be.df.columns)[3:], index=49)
        box_color = st.selectbox(
            'Box color:', list(be.df.columns)[3:], index=127)
        year_box = st.selectbox('Year:', list(range(2010, 2019)), index=8)
    with c2:
        be.create_tree_plot(box_color, box_size, year_box)


