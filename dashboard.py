# ---- Import Libs ---- #
import json
import numpy as np
import pandas as pd
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

# ---- DataFrame ---- #
df = pd.read_csv('./resources/Painel_Covid_2023_Maio.csv', sep=';')
df_states = df[(~df['estado'].isna()) & (df['codmun'].isna())]
df_brasil = df[df['regiao'] == 'Brasil']
df_states.to_csv('./data/df_states.csv')
df_brasil.to_csv('./data/df_brasil.csv')
df_brasil = pd.read_csv('./data/df_brasil.csv')
df_states = pd.read_csv('./data/df_states.csv')

brazil_states = json.load(open('./json/brazil_geo.json', 'r'))

df_states_ = df_states[df_states['data'] == '2020-05-13']
df_data = df_states[df_states['estado'] == 'RJ']

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
)
# ===========================
# Layout

app.layout = dbc.Container(
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(id='logo', src=app.get_asset_url('logo.png'), height=150, width=500),
                html.H5('Evolução COVID-19'),
                dbc.Button('BRASIL', color='primary', id='Location-button',size='lg', style={'font-weight': 'bold'}),
            ], style={}),
            html.P('Informe a data na qual deseja obter informações:', style={'margin-top': '40px'}),
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
            dcc.Graph(id='line-graph', figure=fig_lineBAR),
            dbc.Button('LINKEDIN', color='primary', id='Linkedin', size='lg', href='https://www.linkedin.com/in/ihanmessias/', style={'margin-top': '8px', 'font-weight': 'bold'}), 
            dbc.Button('GITHUB', color='primary', id='Github', size='lg', href='https://www.linkedin.com/in/ihanmessias/', style={'margin-left': '8px', 'margin-top': '8px', 'font-weight': 'bold'}), 
        ]),
        dbc.Col([
            dcc.Graph(id='choropleth-map', figure=fig_map)
        ])
    ])
)

if __name__ == "__main__":
    app.run_server(debug=True)