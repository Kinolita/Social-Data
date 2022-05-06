import plotly.express as px
from utils import *
import streamlit
import plotly.graph_objects as go

labels_co2, labels_en = label_loader()

def format_labels(fig):
    fig.update_layout(
        font_family="Times New Roman",
        font_color="black",
        title_font_family="Times New Roman",
        title_font_color="black",
        legend_title_font_color="black",
        title_font_size=12,
        template='presentation',
    )
    return fig


def create_scatter_plot(df, labels, x='gdp', y='co2', year_filt=2015):
    _df = df[[x, y, 'continent', 'year', 'population', 'country']]
    _df = _df[_df['year'] == year_filt]
    _df.dropna(inplace=True)
    fig = px.scatter(_df, x=x, y=y, color='continent', size="population", size_max=45, log_x=True, log_y=True,
                     title=f"{get_label(labels, y)} <br>vs {get_label(labels, x)}", hover_name='country')


    return streamlit.plotly_chart(format_labels(fig), use_container_width=True)



def choropleth_plot(df, labels, y, year_min=2010):
    _df = df[df['year'] >= year_min]
    fig = px.choropleth(
        _df.sort_values('year'), locations="iso_code",
        color=y,
        hover_name="country",
        color_continuous_scale=px.colors.sequential.Blues,
        animation_frame='year'
    )

    fig.update_layout(
        title_text=get_label(labels, y),
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
    )

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return streamlit.plotly_chart(format_labels(fig), use_container_width=True)







def create_scattermap_plot(df, labels, x='gdp', y='co2_per_capita', year_min=1950):
    _df = df[[x, y, 'continent', 'year', 'population', 'country', 'iso_code']]
    _df = _df[_df['year'] >= year_min]
    _df.dropna(inplace=True)
    fig = px.scatter_geo(_df.sort_values('year'), color=y, size_max=30, locations='iso_code', locationmode='ISO-3',
                     title=f"{get_label(labels, y)}", hover_name='country', animation_frame='year', width=1024, height=500, fitbounds='locations')


    return streamlit.plotly_chart(format_labels(fig), use_container_width=True)


def create_line_plot(df, labels, x='year', y='co2_per_capita', year_min=2000, country_filt=CONTINENTS):
    _df = df.query(f"country in {country_filt}")#[[y, x, 'country']]
    #_df = _df[_df['year'] >= year_min]
    #_df.dropna(inplace=True)
    fig = px.line(_df, x=x, y=y, color='country', title=get_label(labels, y))


    return streamlit.plotly_chart(format_labels(fig), use_container_width=True)


COLS = ['trade_co2', 'cement_co2', 'coal_co2', 'flaring_co2', 'gas_co2', 'oil_co2', 'other_industry_co2', 'year']

def create_line_plot2(df, x='year', y='co2_per_capita', year_min=1950, country_filt='World'):
    _df = df.query(f"country == '{country_filt}'")[COLS]
    _df = _df[_df['year'] >= year_min]
    #_df.dropna(inplace=True)
    fig = px.line(_df, x=x, y=COLS[:-2], title='CO2 emissions from various sources')


    return streamlit.plotly_chart(format_labels(fig), use_container_width=True)