from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1("My first dash application")
])
ratp = pd.read_csv("trafic-annuel-entrant-par-station-du-reseau-ferre-2021.csv", sep=';')


app.layout = (html.Div(children=[
    html.H1("Quelques données "),
    html.H2("Top 10 station"),
    dcc.Graph(
        id='bar-chart',
        figure=px.bar(ratp.sort_values('Trafic', ascending=False).head(10), x='Station', y='Trafic')
    ),
    dcc.Graph(
        id='pie_chart',
        figure=px.pie(ratp.groupby('Ville').sum().sort_values('Trafic', ascending=False).head(5).reset_index(), values='Trafic', names='Ville')
    )

]))


if __name__ == '__main__':
    app.run_server(debug=True)