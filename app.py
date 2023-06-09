from dash import Dash, html, dcc, dependencies
import pandas as pd
import plotly.express as px
app = Dash(__name__)


ratp =pd.read_csv("trafic-annuel-entrant-par-station-du-reseau-ferre-2021.csv", sep=';')
idf = pd.read_csv("emplacement-des-gares-idf.csv", sep=';')
idf[['lat', 'lng']] = idf['Geo Point'].str.split(',', expand=True)
idf['lat'] = idf['lat'].str.strip().astype(float)
idf['lng'] = idf['lng'].str.strip().astype(float)

app.layout = (html.Div(style={'background-color': 'lightgrey'},children=[

    html.H1("Quelques données sur les transports en Ile de France  ",style={'textAlign' : 'center','background':'LightBlue','color': 'white'}),
    html.H2("Information sur la  RATP",style={'textAlign' : 'center','background':'#1ABC9C','color' : 'white'}),
    dcc.Dropdown(
            id='Select_reseau',
            options=[{'label': category, 'value': category} for category in ratp['Réseau'].unique()],
            value=None,
            placeholder='Selectionner un réseau'
        ),

    html.Div(style={'display':'flex','background':'#1ABC9C'},children=[
    dcc.Graph(
        id='bar-chart',
        figure=px.bar(ratp.sort_values('Trafic', ascending=False).head(10), x='Station', y='Trafic')
    ),
    dcc.Graph(
        id='pie-chart',
        figure=px.pie(ratp.groupby('Ville').sum().sort_values('Trafic', ascending=False).head(5).reset_index(), values='Trafic', names='Ville')
    ),
    ]),




    html.H1("Information sur l'ensemble des compagnies  ",style={'center' : 'center','background':'LightBlue','color': 'white'}),
    dcc.Dropdown(
        id='category-filter2',
        options=[{'label': exploitant, 'value': exploitant} for exploitant in idf['exploitant'].unique()],
        value=None,
        placeholder='Selectionne un exploitant',
        ),


html.Div(style={'display':'flex'},children=[
    dcc.Graph(
        id='bar-chart2',
        figure=px.bar(idf.groupby('exploitant'), x=idf.groupby('exploitant').groups.keys(), y=idf.groupby('exploitant').size())
    ),

    dcc.Graph(
        id='bar-chart3',
        figure=px.bar(idf.groupby('ligne'), x=idf.groupby('ligne').groups.keys(), y=idf.groupby('ligne').size()),

    )


    ]),

    html.H2('Carte des stations',style={'textAlign' : 'center','background':'black','color': 'white'}),
    html.Hr(),
    dcc.Graph(
        id="map-graph",
        figure=px.scatter_mapbox(idf, lat='lat',lon='lng',zoom=10,color="exploitant").update_layout(mapbox_style='open-street-map')
    )


]))



@app.callback(
dependencies.Output('bar-chart', 'figure'),
dependencies.Input('Select_reseau', 'value')
)
def update_bar_chart(category):
    if category is None:
        filtered_ratp = ratp
    else:
        filtered_ratp = ratp[ratp['Réseau'] == category]
    return px.bar(filtered_ratp.sort_values('Trafic', ascending=False).head(10),x='Station',y='Trafic',title='Nombre de passagers transportés par ligne ')

@app.callback(
dependencies.Output('pie-chart', 'figure'),
dependencies.Input('Select_reseau', 'value')
)
def update_pie_chart(category):
    if category is None:
        filtered_ratp = ratp
    else:
        filtered_ratp = ratp[ratp['Réseau'] == category]

    return px.pie(filtered_ratp.sort_values(by=['Trafic'],ascending=False).head(10), names='Ville', values='Trafic', title='Trafic Par Ville')



#Call back Graph  IDF
@app.callback(
dependencies.Output('bar-chart2', 'figure'),
[dependencies.Input('category-filter2', 'value')]
)
def update_bar_chart_emp(exploitant):
    if exploitant is None:
        filtered_emp = idf
    else:
        filtered_emp = idf[idf['exploitant'] == exploitant]


    return px.bar(filtered_emp, x=filtered_emp.groupby('exploitant').groups.keys(), y=filtered_emp.groupby('exploitant').size().sort_values(ascending=False), title="Nombre de lignes par exploitant",
                  labels={'x': 'exploitant', 'y': 'Nombre de lignes '})





if __name__ == '__main__':
    app.run_server(debug=True)