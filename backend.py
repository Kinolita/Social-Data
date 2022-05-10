import numpy as np
import plotly.express as px
import utils as utils
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

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


def plot_intro_plot():
    _df = df_temp[df_temp['Entity'] == 'Global']
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Average land-sea temperature anomaly relative to the 1961-1990 avg. temp.", "Global CO2 emissions per Continent"))

    fig.add_trace(go.Line(x=_df['Year'], y=_df['Median temperature anomaly from 1961-1990 average'], name='Avg. Temp'), row=1, col=1)

    _df2 = df.groupby(['continent','year']).sum()['co2'].reset_index()
    for continent in _df2['continent'].unique():
        __df = _df2.query(f'continent == "{continent}"')
        fig.add_trace(go.Scatter(x=__df['year'], y=__df['co2'], name=continent), row=1, col=2)

    fig.update_yaxes(title_text="Global average temperature", row=1, col=1)
    fig.update_yaxes(title_text="Emissions of CO2, in million tonnes", row=1, col=2)
    fig.update_traces(hovertemplate="%{y}")
    fig.update_layout(showlegend=False)

    return st.plotly_chart(format_labels(fig), use_container_width=True)

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
    fig.update_layout(
        font_color='white',
        title_font_color='white')
    fig.update_layout(title_x=0.1)
    return fig


def create_scatter_plot(x, y, hover, color='continent', size='population', year_min=MIN_YEAR, animate=True):
    _df = df[[x, y, size, color, 'year', 'iso_code', 'country']]
    _df = _df[_df['year'] >= year_min]
    _df.dropna(inplace=True)
    if animate:
        fig = px.scatter(
            _df, x=x, y=y,
            color=color,
            size=size,
            size_max=45,
            log_x=True, log_y=True,
            animation_frame='year',
            custom_data=['country'],
            title=f"{utils.get_label(LABELS, y)} <br>vs {utils.get_label(LABELS, x)}"

        )
        fig = get_last_frame(fig)

    else:
        fig = px.scatter(
            _df.query('year == 2016'), x=x, y=y,
            color=color,
            size=size,
            size_max=45,
            log_x=True, log_y=True,
            custom_data=['country'],
            title=f"{utils.get_label(LABELS, y)} <br>vs {utils.get_label(LABELS, x)}"

        )

    fig.update_traces(hovertemplate=hover) #


    return st.plotly_chart(format_labels(fig), use_container_width=True)



def choropleth_plot(y, year_min=MIN_YEAR):
    _df = df[df['year'] >= year_min]
    _df = _df[(_df['country'] != 'World') & (_df['country'] != 'World') & (_df['country'] != 'Asia Pacific') & (_df['country'] != 'OECD') & (_df['country'] != 'CIS') & (_df['country'] != 'Middle East') & (_df['country'] != 'Non-OECD')]
    fig = px.choropleth(
        _df.sort_values('year'),
        locations="iso_code",
        color=y,
        hover_name="country",
        color_continuous_scale='RdBu_r',
        range_color=[np.min(_df[y]), np.max(_df[y])],
        animation_frame='year',
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
    # fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
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



def create_tree_plot(x, y, year=2018):
    _df = df.query(f'year == {year}')[[y, x, 'iso_code', 'country', 'continent']].dropna()
    fig = px.treemap(_df, path=[px.Constant("world"), 'continent', 'country'], values=y,
                     color=x, color_continuous_scale='RdBu_r',
                     )
    fig.update_traces(hovertemplate='<b>%{label} </b> <br>Box Color: %{color:.2f} <br>Box Size: %{value:.2f}') #

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
    fig.update_layout(xaxis=dict(showgrid=False),
                      yaxis=dict(showgrid=False)
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
    _df = df.query(f'year in {[year - window_size, year]}')[[y, x, 'iso_code', 'country', 'continent', 'year']].dropna()
    _df.set_index(['continent', 'country'], inplace=True)

    _df_old = _df[_df['year'] == year - window_size]
    _df_now = _df[_df['year'] == year]

    cmap = 'RdBu' if reverse else 'RdBu_r'
    _df_now['change %'] = _df_now[x] - _df_old[x]
    _df_now['change_co2'] = _df_now[y] - _df_old[y]

    print(_df_old)
    print(_df_now)
    fig = px.treemap(
        _df_now.reset_index(),
         path=[px.Constant('world'), 'continent', 'country'],
         values=y,
         color='change %', color_continuous_scale=cmap,
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


def create_energy_consumption_source():
    labels = ['biofuel_consumption', 'coal_consumption', 'gas_consumption', 'hydro_consumption', 'nuclear_consumption', 'oil_consumption', 'other_renewable_consumption', 'solar_consumption', 'wind_consumption']
    _df = df[['year', 'biofuel_consumption', 'coal_consumption', 'country', 'gas_consumption', 'hydro_consumption', 'nuclear_consumption', 'oil_consumption', 'other_renewable_consumption', 'solar_consumption', 'wind_consumption']].dropna()
    _df = _df[(_df['country'] != 'World') & (_df['country'] != 'World') & (_df['country'] != 'Asia Pacific') & (_df['country'] != 'OECD') & (_df['country'] != 'CIS') & (_df['country'] != 'Middle East') & (_df['country'] != 'Non-OECD')]
    _df = _df.drop(['country'], axis=1)
    _df = _df.groupby('year').sum().reset_index()
    _df.columns = ['year'] + [f"{('_'.join(x.split('_')[:-1])).capitalize()}" for x in _df.columns.to_list()[1:]]
    _df = pd.melt(_df, id_vars=['year'], value_vars=_df.columns.to_list()[1:])


    fig = px.area(_df.query('year >= 2010'), x="year", y="value", color="variable", line_group="variable")
    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Year",
        yaxis_title="Energy Consumption (TW/h)",
        legend_title='Source',
        legend_traceorder="reversed"
    )
    fig.update_traces(hovertemplate='%{y:.2f} TW/h')

    return st.plotly_chart(format_labels(fig), use_container_width=True)


def create_lineplot_change_subplots(current_year, window_size):
    ys = ['fossil_share_energy', 'renewables_share_energy']
    titles = ['Change in Fossil Energy Share', 'Change in Renewables Energy Share']
    _df = df.query(f'year in {[current_year-window_size, current_year]}')[ys + ['year', 'iso_code', 'country', 'population', 'continent']]

    fig = make_subplots(rows=1, cols=2, subplot_titles=titles)

    # fig.update_yaxes(type="log")

    changes = []

    for idx, y in enumerate(ys):

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
                                     line=dict(color=c, width=w), name=country, hovertext=change), row=1, col=idx+1)
            if world:
                fig.add_annotation(x=df_c['year'].iloc[1], y=df_c[y].iloc[1],
                                   text="World",
                                   font_color='red',
                                   showarrow=False,
                                   xshift=20, row=1, col=idx+1)

            fig.update_layout(
                geo=dict(
                    showframe=False,
                    showcoastlines=False,
                    projection_type='equirectangular'
                ),
            )
        fig.add_vline(x=2016, line_width=2, line_color="black", row=1, col=idx+1)
        fig.add_vline(x=2020, line_width=2, line_color="black", row=1, col=idx+1)
        fig.update_xaxes(showgrid=False, row=1, col=idx+1)
        fig.update_yaxes(showgrid=False, range=[-10,110], row=1, col=idx+1, zeroline=False)
        fig.update_xaxes(title_text="", range=[2015, 2021], tickvals=[2016, 2020], row=1, col=idx+1)
    fig.update_yaxes(title_text="Share of Total Energy Consumption", row=1, col=1)
    fig.update_layout(showlegend=False)

    return st.plotly_chart(format_labels(fig), use_container_width=True)
