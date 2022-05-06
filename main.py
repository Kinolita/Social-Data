import pandas as pd
import streamlit
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from backend import *
from utils import *

df_co2, df_en, df_temp = data_loader()
labels_co2, labels_en = label_loader()


st.set_page_config(page_title="Friends • The Network",layout='wide')


st.title('Welcome to the project website for the course Social graphs and interactions (02805)')
st.subheader('Made by Adrienne, Usama, and Ferenc')



with st.container():


    col1, col2, col3 = st.columns(3)

    with col1:
        col1.header('Scatterplot')

        x_selected = st.selectbox('x-axis:', list(df_co2.columns)[2:], index=len(df_co2.columns)-7)
        y_selected = st.selectbox('y-axis:', list(df_co2.columns)[3:], index=0)

        create_scatter_plot(df_co2, x=x_selected, y=y_selected)

    with col2:
        col2.header('Sentiment for each director')

    """
    Speaking about roller coaster rides… The Friends viewers have also been on a bit of a ride.
    The episode with the lowest overall sentiment was Episode 1 in Season 4: _The one with the Jellyfish_, as you probably remember.
    The crazy thing is that in the same season we have one of the highest sentiment scores of an episode - Episode 5: _The one with Joey's new girlfriend_.
    """


