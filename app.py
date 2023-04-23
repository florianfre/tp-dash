from dash import Dash, html, dcc, dependencies
import pandas as pd
import plotly.express as px
app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1("My first dash application")
])
ratp =pd.read_csv("trafic-annuel-entrant-par-station-du-reseau-ferre-2021.csv", sep=';')
idf = pd.read_csv("emplacement-des-gares-idf.csv", sep=';')

app.layout = (html.Div(children=[
    html.H1("Quelques données "),
    html.H2("Top 10 station"),
    dcc.Dropdown(
            id='Select_reseau',
            options=[{'label': category, 'value': category} for category in ratp['Réseau'].unique()],
            value=None,
            placeholder='Selectionner un réseau'
        ),
    dcc.Graph(
        id='bar-chart',
        figure=px.bar(ratp.sort_values('Trafic', ascending=False).head(10), x='Station', y='Trafic')
    ),
    dcc.Graph(
        id='pie-chart',
        figure=px.pie(ratp.groupby('Ville').sum().sort_values('Trafic', ascending=False).head(5).reset_index(), values='Trafic', names='Ville')
    ),






    dcc.Dropdown(
        id='category-filter2',
        options=[{'label': exploitant, 'value': exploitant} for exploitant in idf['exploitant'].unique()],
        value=None,
        placeholder='Selectionne un exploitant',
        ),

    dcc.Graph(
        id='bar-chart2',
        figure=px.bar(idf.groupby('exploitant'), x=idf.groupby('exploitant').groups.keys(), y=idf.groupby('exploitant').size())
    ),

    dcc.Graph(
        id='bar-chart3',
        figure=px.bar(idf.groupby('ligne'), x=idf.groupby('ligne').groups.keys(), y=idf.groupby('ligne').size())
    ),



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
    return px.bar(filtered_ratp.sort_values('Trafic', ascending=False).head(10),x='Station',y='Trafic',title='bar-chart')

@app.callback(
dependencies.Output('pie-chart', 'figure'),
dependencies.Input('Select_reseau', 'value')
)
def update_pie_chart(category):
    if category is None:
        filtered_ratp = ratp
    else:
        filtered_ratp = ratp[ratp['Réseau'] == category]

    return px.pie(filtered_ratp.sort_values(by=['Trafic'],ascending=False).head(10), names='Ville', values='Trafic', title='Pie chart')



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