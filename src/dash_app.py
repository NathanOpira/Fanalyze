import pandas as pd
from datetime import datetime

import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Getting today's file.
today = datetime.now().strftime("%Y-%m-%d")
data_path = f"data/processed/google_trends_cleaned_{today}.csv"

# Loading data.
df = pd.read_csv(data_path, index_col=0, parse_dates=True)

# App init.
app = dash.Dash(__name__)
app.title = "Fanalyze Dashboard"

# Layout.
app.layout = html.Div([
    html.H1("📈 Fanalyze: African Footballer Popularity Trends", style={"textAlign": "center"}),

    dcc.Dropdown(
        id='player-dropdown',
        options=[{"label": player, "value": player} for player in df.columns],
        value=["Mohamed Salah", "Achraf Hakimi"],
        multi=True,
        placeholder="Select players to compare...",
        style={"margin": "20px"}
    ),

    dcc.Graph(id='trend-graph')
])

# Callback.
@app.callback(
    Output('trend-graph', 'figure'),
    [Input('player-dropdown', 'value')]
)
def update_graph(selected_players):
    if not selected_players:
        return px.line(title="No players selected.")

    fig = px.line(df[selected_players],
                  labels={"value": "Popularity", "index": "Date"},
                  title="Google Search Trends (Last 3 Months)")
    fig.update_layout(legend_title_text='Players')
    return fig

# Run.
if __name__ == "__main__":
    app.run(debug=True)