import numpy as np
import plotly.express as px
import utils as utils
#from utils import *
import streamlit
import plotly.graph_objects as go

COLS = ['trade_co2', 'cement_co2', 'coal_co2', 'flaring_co2', 'gas_co2', 'oil_co2', 'other_industry_co2', 'year']

LABELS = utils.label_loader()
MIN_YEAR = 2010

def get_last_frame(fig):
    last_frame_num = int(len(fig.frames) -1)
    fig.layout['sliders'][0]['active'] = last_frame_num
    _fig = go.Figure(data=fig['frames'][last_frame_num]['data'], frames=fig['frames'], layout=fig.layout)
    return _fig

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
    fig.update_layout(title_x=0.1)
    return fig


def create_scatter_plot(df, x, y, labels=LABELS, year_min=MIN_YEAR):
    _df = df[[x, y, 'continent', 'year', 'population', 'country']]
    _df = _df[_df['year'] >= year_min]
    _df.dropna(inplace=True)
    fig = px.scatter(
        _df, x=x, y=y,
        color='continent',
        size="population",
        size_max=45,
        log_x=True, log_y=True,
        hover_name='country',
        animation_frame='year',
        title=f"{utils.get_label(labels, y)} <br>vs {utils.get_label(labels, x)}"
    )

    fig = get_last_frame(fig)
    # fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0})

    return streamlit.plotly_chart(format_labels(fig), use_container_width=True)



def choropleth_plot(df, y, labels=LABELS, year_min=MIN_YEAR):
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

    fig = get_last_frame(fig)
    #fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return streamlit.plotly_chart(format_labels(fig), use_container_width=True)




def create_scattermap_plot(df, x, y, labels, year_min=MIN_YEAR):
    _df = df[[x, y, 'continent', 'year', 'population', 'country', 'iso_code']]
    _df = _df[_df['year'] >= year_min]
    _df.dropna(inplace=True)
    fig = px.scatter_geo(_df.sort_values('year'), color=y, size_max=30, locations='iso_code', locationmode='ISO-3',
                     title=f"{get_label(labels, y)}", hover_name='country', animation_frame='year', width=1024, height=500, fitbounds='locations')



    return streamlit.plotly_chart(format_labels(fig), use_container_width=True)


def create_line_plot(df, y='co2_per_capita', labels=LABELS, year_min=MIN_YEAR, country_filt=CONTINENTS):
    _df = df.query(f"country in {country_filt}")#[[y, x, 'country']]
    _df = _df[_df['year'] >= year_min]
    #_df.dropna(inplace=True)
    fig = px.line(_df.sort_values(['year', y], ascending=False), x='year', y=y, color='country', title=get_label(labels, y))


    #fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return streamlit.plotly_chart(format_labels(fig), use_container_width=True)



def create_line_plot2(df, x='year', y='co2_per_capita', year_min=MIN_YEAR, country_filt='World'):
    _df = df.query(f"country == '{country_filt}'")[COLS]
    _df = _df[_df['year'] >= year_min]
    #_df.dropna(inplace=True)
    fig = px.line(_df, x=x, y=COLS[:-2], title='CO2 emissions from various sources')


    return streamlit.plotly_chart(format_labels(fig), use_container_width=True)



def create_tree_plot(df, x, y):
    _df = df.query('year == 2018')[[y, x, 'iso_code', 'country', 'population', 'continent', 'gdp', 'renewables_energy_per_capita']].dropna()
    fig = px.treemap(_df, path=[px.Constant("world"), 'continent', 'country'], values=y,
                     color=x, hover_data=['iso_code'],
                     color_continuous_scale='RdBu',
                     color_continuous_midpoint=np.average(_df[x], weights=_df[y])
                     )
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    return streamlit.plotly_chart(format_labels(fig), use_container_width=True)
