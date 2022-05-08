import numpy as np
import plotly.express as px
import utils as utils
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

LABELS = utils.label_loader()
CONTINENTS = ['World', 'Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania', 'Antarctica']
COLS = ['trade_co2', 'cement_co2', 'coal_co2', 'flaring_co2', 'gas_co2', 'oil_co2', 'other_industry_co2', 'year']

MIN_YEAR = 2010


df, df_temp, df_energy_dist = utils.data_loader()

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
        template='plotly_white',
    )
    fig.update_layout(title_x=0.1)
    return fig


def create_scatter_plot(x, y, year_min=MIN_YEAR):
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
        title=f"{utils.get_label(LABELS, y)} <br>vs {utils.get_label(LABELS, x)}"

    )

    fig = get_last_frame(fig)
    # fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0})

    return st.plotly_chart(format_labels(fig), use_container_width=True)



def choropleth_plot(y, year_min=MIN_YEAR):
    _df = df[df['year'] >= year_min]
    fig = px.choropleth(
        _df.sort_values('year'), locations="iso_code",
        color=y,
        hover_name="country",
        color_continuous_scale=px.colors.sequential.Blues,
        animation_frame='year'
    )

    fig.update_layout(
        title_text=utils.get_label(LABELS, y),

        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
    )

    fig = get_last_frame(fig)
    #fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return st.plotly_chart(format_labels(fig), use_container_width=True)




def create_scattermap_plot(x, y, year_min=MIN_YEAR):
    _df = df[[x, y, 'continent', 'year', 'population', 'country', 'iso_code']]
    _df = _df[_df['year'] >= year_min]
    _df.dropna(inplace=True)
    fig = px.scatter_geo(_df.sort_values('year'), color=y, size_max=30, locations='iso_code', locationmode='ISO-3',
                     title=f"{utils.get_label(LABELS, y)}", hover_name='country', animation_frame='year', width=1024, height=500, fitbounds='locations')




    return st.plotly_chart(format_labels(fig), use_container_width=True)


def create_line_plot(y='co2_per_capita', year_min=MIN_YEAR, country_filt=CONTINENTS):
    _df = df.query(f"country in {country_filt}")#[[y, x, 'country']]
    _df = _df[_df['year'] >= year_min]
    #_df.dropna(inplace=True)
    fig = px.line(_df.sort_values(['year', y], ascending=False), x='year', y=y, color='country', title=utils.get_label(LABELS, y))



    #fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return st.plotly_chart(format_labels(fig), use_container_width=True)



# def create_line_plot2(df, x='year', y='co2_per_capita', year_min=MIN_YEAR, country_filt='World'):
#     _df = df.query(f"country == '{country_filt}'")[COLS]
#     _df = _df[_df['year'] >= year_min]
#     #_df.dropna(inplace=True)
#     fig = px.line(_df, x=x, y=COLS[:-2], title='CO2 emissions from various sources')
#
#
#     return streamlit.plotly_chart(format_labels(fig), use_container_width=True)



def create_tree_plot(x, y):
    _df = df.query('year == 2018')[[y, x, 'iso_code', 'country', 'population', 'continent', 'gdp', 'renewables_energy_per_capita']].dropna()
    fig = px.treemap(_df, path=[px.Constant("world"), 'continent', 'country'], values=y,
                     color=x, hover_data=['iso_code'],
                     color_continuous_scale='RdBu_r',
                     )
    fig.update_traces(hovertemplate='<b>%{label} </b> <br>Fossil Energy: %{color:.2f}% <br>CO2 per capita: %{value:.2f}') #

    # fig.update_layout(
    #     hoverlabel=dict(
    #         bgcolor="white",
    #         font_size=16,
    #         font_family="Rockwell"
    #     )
    # )
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    return st.plotly_chart(format_labels(fig), use_container_width=True)


def create_lineplot_change(y, current_year, window_size):
    _df = df.query(f'year in {[current_year-window_size, current_year]}')[[y, 'year', 'iso_code', 'country', 'population', 'continent']]

    fig = go.Figure()
    fig.add_vline(x=current_year - window_size, line_width=2, line_color="black")
    fig.add_vline(x=current_year, line_width=2, line_color="black")
    # fig.update_yaxes(type="log")

    changes = []

    for country in _df['country'].unique():
        df_c = _df[_df['country'] == country].sort_values('year')

        try:
            change = np.round(df_c.iloc[1][y] - df_c.iloc[0][y], 3)
        except Exception as e:
            change = np.nan

    #    df_c['change'] = [0, change]
        changes.append(change)
        # Create and style traces
        if country == 'World':
            c = 'red'
            w = 3
            world = True
        else:
            c = 'white'
            w = 1
            world = False
        fig.add_trace(go.Scatter(x=df_c['year'], y=df_c[y],
                                 line=dict(color=c, width=w), name=country, hovertext=change))
        if world:
            fig.add_annotation(x=df_c['year'].iloc[1], y=df_c[y].iloc[1],
                               text="World",
                               showarrow=False,
                               xshift=20)


    fig.update_layout(showlegend=False)
    fig.update_layout(
        title_text=f"{utils.get_label(LABELS, y)} - global change: {np.nanmean(changes)}",
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
    )
    return st.plotly_chart(format_labels(fig), use_container_width=True)


def create_emission_pie():
    _df = df_energy_dist.copy()

    fig = go.Figure(go.Sunburst(
        name = "",
        ids = _df['ids'],
        labels = _df['labels'],
        parents = _df['parents'],
        values=_df['share'],
        branchvalues="total",
        marker=dict(
            colors=_df['share'],
            colorscale='RdBu_r',
            cmid=_df['share'].mean()),
        hovertemplate='<b>%{label}: %{value:.2f}%',
        hoverinfo="none"
    ))

    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    # fig.update_layout(uniformtext=dict(minsize=10, mode='hide'))

    return st.plotly_chart(format_labels(fig), use_container_width=True)


def create_paris_agreement_nations():
    df = utils.get_current_member_countries()
    fig = px.treemap(df, path=[px.Constant("world"), 'Country'], values="Percentage of greenhousegases for ratification",
                     color_continuous_scale='RdBu_r',
                     )
    fig.update_traces(hovertemplate='<b>%{label} </b> <br>Fossil Energy: %{color:.2f}% <br>CO2 per capita: %{value:.2f}') #

    # fig.update_layout(
    #     hoverlabel=dict(
    #         bgcolor="white",
    #         font_size=16,
    #         font_family="Rockwell"
    #     )
    # )
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    return st.plotly_chart(format_labels(fig), use_container_width=True)


def create_tree_plot_window(x, y, year, window_size, hover, reverse=False):
    _df = df.query(f'year in {[year - window_size, year]}')[[y, x, 'iso_code', 'country', 'population', 'continent', 'gdp', 'renewables_energy_per_capita', 'year']].dropna()
    _df.set_index(['continent', 'country'], inplace=True)

    _df_old = _df[_df['year'] == year - window_size]
    _df_now = _df[_df['year'] == year]

    cmap = 'RdBu' if reverse else 'RdBu_r'
    _df_now['change'] = _df_now[x] - _df_old[x]
    _df_now['change_co2'] = _df_now[y] - _df_old[y]

    print(_df_old)
    print(_df_now)
    fig = px.treemap(_df_now.reset_index(), path=[px.Constant('world'), 'continent', 'country'], values=y,
                     color='change', color_continuous_scale=cmap,
                     )
    fig.update_traces(hovertemplate=hover) #

    # fig.update_layout(
    #     hoverlabel=dict(
    #         bgcolor="white",
    #         font_size=16,
    #         font_family="Rockwell"
    #     )
    # )
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    return st.plotly_chart(format_labels(fig), use_container_width=True)
