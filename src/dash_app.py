from utils import get_player_summary

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
    html.Div([
        html.Img(src="/assets/logo.jpg", style={"height": "60px", "marginRight": "15px"})
        html.H1("Fanalyze: African Footballer Popularity Trends"),
    ],  style={
        "display": "flex",
        "alignItems": "center",
        "backgroundColor": "#0F172A",
        "padding": "15px",
        "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.2)",
    }),

    dcc.Dropdown(
        id='player-dropdown',
        options=[{"label": player, "value": player} for player in df.columns],
        value=["Mohamed Salah", "Achraf Hakimi"],
        multi=True,
        placeholder="Select players to compare...",
        style={"margin": "20px"}
    ),

    dcc.Graph(id='trend-graph'),

    html.Div(
        id='player-summary-container',
        style={"display": "flex", "justifyContent": "space-around", "margin": "40px"}
    ),

    html.Footer(
        "© 2025 Fanalyze. Built by Nate 🇺🇬",
        style={
            "textAlign": "center",
            "padding": "20px",
            "color": "#9CA3AF",
            "backgroundColor": "#0F172A"
        }
    ),
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
    fig.update_layout(
        plot_bgcolor='#1F2937',
        paper_bgcolor='#1F2937',
        font=dict(color='#F9FAFB'),
        title_font_size=24,
        legend=dict(bgcolor='#111827', bordercolor='gray', borderwidth=1)
    )
    return fig

@app.callback(
    Output('player-summary-container', 'children'),
    Input('player-dropdown', 'value')
)
def update_player_summary(selected_players):
    if not selected_players:
        return []

    summaries = []
    for player in selected_players[:2]:  # only first two
        stats = get_player_summary(df, player)
        card = html.Div([
            html.H3(stats['name']),
            html.P(f"Avg (last 7 days): {stats['avg_score']}"),
            html.P(f"Peak: {stats['peak_score']} on {stats['peak_date']}"),
            html.P(f"Spike count (>80): {stats['spike_count']}"),
        ], className="card")
        summaries.append(card)

    return summaries

# Run.
if __name__ == "__main__":
    app.run(debug=True)