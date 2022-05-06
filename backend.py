import plotly.express as px
from utils import *
import streamlit

labels_co2, labels_en = label_loader()

def create_scatter_plot(df, x='gdp', y='co2', year_filt=2015):
    _df = df[[x, y, 'continent', 'year', 'population', 'country']]
    _df = _df[_df['year'] == year_filt]
    _df.dropna(inplace=True)
    fig = px.scatter(_df, x=x, y=y, color='continent', size="population", size_max=45, log_x=True, log_y=True,
                     title=f"{get_label(labels_co2, y)} <br>vs {get_label(labels_co2, x)}", hover_name='country', template='presentation')


    return streamlit.plotly_chart(fig, use_container_width=True)