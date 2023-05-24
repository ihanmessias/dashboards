# ---- Import Libs ---- #
import json
import numpy as np
import pandas as pd
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

# ---- DataFrame ---- #
# df = pd.read_csv('./resources/Painel_Covid_2023_Maio.csv', sep=';')
# df_states = df[(~df['estado'].isna()) & (df['codmun'].isna())]
# df_brasil = df[df['regiao'] == 'Brasil']
# df_states.to_csv('./data/df_states.csv')
# df_brasil.to_csv('./data/df_brasil.csv')
df_brasil = pd.read_csv('./data/df_brasil.csv')
df_states = pd.read_csv('./data/df_states.csv')

brazil_states = json.load(open('./json/brazil_geo.json', 'r'))

df_states_ = df_states[df_states['data'] == '2020-05-13']
df_data = df_states[df_states['estado'] == 'RJ']

select_columns = {"casosAcumulado":'Casos Acumulados',
                  "casosNovos": 'Novos Casos',
                  "obitosAcumulado":'Óbitos Totais',
                  "obitosNovos":'Óbitos por dia'}
# ---- Dashboard ---- #
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

fig_map = px.choropleth_mapbox(df_states_, locations='estado', color='casosNovos',
                           center={'lat': -16.95, 'lon': -47.78},
                           geojson=brazil_states,color_continuous_scale='Redor', opacity=0.4,
                           hover_data={'casosAcumulado':True,'casosNovos':True,'obitosNovos':True,'estado':True})
fig_map.update_layout(
    paper_bgcolor='#242424',
    autosize=True,
    margin=go.layout.Margin(l=0,r=0,t=0,b=0),
    showlegend=False,
    mapbox_style='carto-darkmatter'
)

fig_lineBAR = go.Figure(layout={'template':'plotly_dark'})
fig_lineBAR.add_trace(go.Scatter(x=df_data['data'], y=df_data['casosAcumulado']))
fig_lineBAR.update_layout(
    paper_bgcolor='#242424',
    plot_bgcolor='#242424',
    autosize=True,
    margin=go.layout.Margin(l=10,r=10,t=10,b=10),
    height=300,
    width=760
)
# ===========================
# Layout

app.layout = dbc.Container(
    dbc.Row([
        # Primeira Coluna
        dbc.Col([
            html.Div([
                html.Img(id='logo', src=app.get_asset_url('logo.png'), height=100, width=455),
                html.H5('Evolução COVID-19', style={'font-weight': 'bold'}),
                dbc.Button('BRASIL', color='primary', id='Location-button',size='lg', style={'font-weight': 'bold'}),
            ], style={}),
            html.P('Informe a data na qual deseja obter informações:', style={'font-size':'16px','margin-top': '18px'}),
            html.Div(id='div-test', children=[
               dcc.DatePickerSingle(
                   id='date-picker',
                   min_date_allowed=df_brasil['data'].min(),
                   max_date_allowed=df_brasil['data'].max(),
                   date=df_brasil['data'].max(),
                   display_format='MMMM D, YYYY',
                   style={'border': '8px solid black'} 
               )
            ]),
            # Box:
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span('Casos recuperados'),
                            html.H3(style={'color': '#adfc92'}, id='casos-recuperados-text'),
                            html.Span('Em acompanhamento'),
                            html.H5(id='em-acompanhamento-text')
                        ])
                    ], color='light', outline=True,
                            style={'margin-top': '10px',
                                'box-shadow': '0 4px 4px 0 rgba(0,0,0,0.15), 0 4px 20px 0 rgba(0,0,0,0.19)',
                                'color': '#FFFFFF'})
                ], md=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span('Casos confirmados totais'),
                            html.H3(style={'color': '#389fd6'}, id='casos-confirmados-text'),
                            html.Span('Novos casos na data'),
                            html.H5(id='novos-casos-text')
                        ])
                    ], color='light', outline=True,
                            style={'margin-top': '10px',
                                    'box-shadow': '0 4px 4px 0 rgba(0,0,0,0.15), 0 4px 20px 0 rgba(0,0,0,0.19)',
                                    'color': '#FFFFFF'})
                ], md=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span('Óbitos confirmados'),
                            html.H3(style={'color': '#DF2935'}, id='obitos-text'),
                            html.Span('Óbitos na data'),
                            html.H5(id='obitos-na-data-text')
                        ])
                    ], color='light', outline=True,
                            style={'margin-top': '10px',
                                'box-shadow': '0 4px 4px 0 rgba(0,0,0,0.15), 0 4px 20px 0 rgba(0,0,0,0.19)',
                                'color': '#FFFFFF'})
                ], md=4)
            ]),
            #====
                html.Div([
                    html.P('Selecione que tipo de dado deseja visualizar:', style={'font-size':'16px','margin-top': '18px'}),
                    dcc.Dropdown(id='location-dropdown',
                                options=[{'label': j, 'value': i} for i, j in select_columns.items()],
                                value='casosNovos',
                                style={'margin-top': '10px'}
                                ),
                    dcc.Graph(id='line-graph', figure=fig_lineBAR),
            ]),
            html.P('Entre em contato comigo:', style={'font-size':'16px','color':'cyan','margin-top': '18px'}),
            dbc.Button('LINKEDIN', color='warning', id='Linkedin', size='lg', href='https://www.linkedin.com/in/ihanmessias/', style={'font-size':'14px','color':'black','margin-top':'5px','font-weight':'bold','padding':'8px 40px 8px 40px'}), 
            dbc.Button('GITHUB', color='warning', id='Github', size='lg', href='https://github.com/mrhowaito', style={'font-size':'14px','color':'black','margin-left':'8px','margin-top':'5px','font-weight':'bold','padding': '8px 40px 8px 40px'}), 
            dbc.Button('INSTAGRAM', color='warning', id='Instagram', size='lg', href='https://www.instagram.com/devlinuxtv/', style={'font-size':'14px','color':'black','margin-left':'8px','margin-top':'5px','font-weight':'bold','padding': '8px 40px 8px 40px'}), 
        ], md=5, style={'padding': '25px', 'background-color': '#242424'}),
        # Segunda Coluna
        dbc.Col([
            dcc.Graph(id='choropleth-map', figure=fig_map)
        ], md=7)
    ], className='g-0')
,fluid=True)

if __name__ == "__main__":
    app.run_server(debug=True)