from utils import get_player_summary

import pandas as pd
from datetime import datetime

import dash
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# Getting today's file.
today = datetime.now().strftime("%Y-%m-%d")
data_path = f"data/processed/google_trends_cleaned_{today}.csv"

# Loading data.
df = pd.read_csv(data_path, index_col=0, parse_dates=True)

# inserting players' metadata.
player_metadata = {
    "Ilaix Moriba": {
        "club": "RB Leipzig",
        "country": "🇬🇳 Guinea",
        "position": "Midfielder",
        "bio": "Highly rated for his strength and passing at a young age.",
        "youtube_url": "https://youtu.be/TnQF8Fk9RzM?si=RD5LsVcF4GJzoGbc"
    },
    "Kamaldeen Sulemana": {
        "club": "Southampton",
        "country": "🇬🇭 Ghana",
        "position": "Winger",
        "bio": "Electric speed and raw dribbling talent define his game.",
        "youtube_url": "https://youtu.be/f8B6vvOpuAA?si=Bfnd81qcHsWhFutt"
    },
    "Carlos Baleba": {
        "club": "Brighton & Hove Albion",
        "country": "🇨🇲 Cameroon",
        "position": "Midfielder",
        "bio": "Box-to-box engine with strong defensive instincts.",
        "youtube_url": "https://youtu.be/8vAYT5eToNg?si=vLDBOpVU1jxZNiOl"
    },
    "Bryan Mbuemo": {
        "club": "Brentford",
        "country": "🇨🇲 Cameroon",
        "position": "Forward",
        "bio": "Smart finisher and creative force in the Premier League.",
        "youtube_url": "https://youtu.be/-aCFZZ1W_Kw?si=MfFtQNXbMQAic2Fb"
    },
    "Ismaila Sarr": {
        "club": "Olympique Marseille",
        "country": "🇸🇳 Senegal",
        "position": "Winger",
        "bio": "Explosive pace and goal threat on the flanks.",
        "youtube_url": "https://youtu.be/W8APfDm23iM?si=-t0aX8FmWV9dV2v6"
    },
    "Mohamed Salah": {
        "club": "Liverpool",
        "country": "🇪🇬 Egypt",
        "position": "Forward",
        "bio": "Global icon known for scoring, speed and leadership.",
        "youtube_url": "https://youtu.be/wwAtHUc0Pzk?si=0Qv6-nMHRrOP8AC4"
    },
    "Samuel Chukweze": {
        "club": "AC Milan",
        "country": "🇳🇬 Nigeria",
        "position": "Winger",
        "bio": "Left-footed dribbler with flair and pace to burn.",
        "youtube_url": "https://youtu.be/Rsa5SfMtRxs?si=4P06LBY_D3-3inda"
    },
    "Antoine Semenyo": {
        "club": "Bournemouth",
        "country": "🇬🇭 Ghana",
        "position": "Forward",
        "bio": "Direct attacker with strength and energy up front.",
        "youtube_url": "https://youtu.be/7NurJqDBdA0?si=EMK_dHGMjCahpopH"
    },
    "Achraf Hakimi": {
        "club": "Paris Saint-Germain",
        "country": "🇲🇦 Morocco",
        "position": "Right-back",
        "bio": "Lightning fast fullback, a threat at both ends.",
        "youtube_url": "https://youtu.be/wyadspWNnlY?si=8TDsIw3Kn1MyoHkR"
    },
    "Ademola Lookman": {
        "club": "Atalanta",
        "country": "🇳🇬 Nigeria",
        "position": "Winger",
        "bio": "Versatile attacker with an eye for spectacular goals.",
        "youtube_url": "https://youtu.be/QTw8WYxpVCs?si=-JDXd45dxNFY56eB"
    },
    "Serhou Guirassy": {
        "club": "VfB Stuttgart",
        "country": "🇬🇳 Guinea",
        "position": "Striker",
        "bio": "Aerial threat and clinical finisher in the Bundesliga.",
        "youtube_url": "https://youtu.be/VkotyZtg-2o?si=lJDqzsUHeG_Gj44J"
    },
    "Bilal El Khannouss": {
        "club": "Genk",
        "country": "🇲🇦 Morocco",
        "position": "Midfielder",
        "bio": "Young creator with strong vision and technique.",
        "youtube_url": "https://youtu.be/v9jdV1M6_lc?si=3t7jgBFJmHwpdkpX"
    },
    "Mohammed Kudus": {
        "club": "West Ham United",
        "country": "🇬🇭 Ghana",
        "position": "Midfielder",
        "bio": "Explosive dribbler, equally strong as creator and scorer.",
        "youtube_url": "https://youtu.be/hv_iAX3j6lc?si=4kmfq7owMGpfqJqT"
    }
}

# App init.
app = dash.Dash(__name__)
app.title = "Fanalyze Dashboard"

# Layout.
app = Dash(__name__, external_stylesheets=["https://fonts.googleapis.com/css2?family=Teko:wght@400;600&display=swap"
])
app.layout = html.Div([
    dcc.Store(id='clicked-player'),
    html.Div([
        html.Img(src="/assets/logo.jpg",
                 style={
                     "height": "60px",
                     "marginRight": "15px"}),
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

    html.Div([
        html.Div(
            id='trend-graph-container',
            children=[dcc.Graph(id='trend-graph')],
            style={"flex": "2", "padding": "10px"}
        ),
        html.Div(
            id='trending-player-card',
            style={"flex": "1", "padding": "10px"}
        )
    ], style={
       "display": "flex",
       "flexWrap": "wrap",
       "justifyContent": "space-between",
       "alignItems": "flex-start",
       "marginTop": "30px"
    }),

    html.Div(
        id='fan-buzz',
        style={
            "backgroundColor": "#121212",
            "color": "#f2f2f2",
            "padding": "20px",
            "borderRadius": "10px",
            "marginTop": "30px",
            "boxShadow": "0 0 8px #00ff99",
            "maxWidth": "500px",
            "fontFamily": "Teko, sans-serif",
            "fontSize": "18px"
        }
    ),

    html.Div(
        id='leaderboard-container',
        style={
           "marginTop": "40px",
           "padding": "20px",
           "backgroundColor": "#121212",
           "borderRadius": "10px",
           "boxShadow": "0 0 10px #00ff99"
        }
    ),

    html.Div(
        id='player-info-container',
        style={
            "marginTop": "30px",
            "padding": "20px",
            "backgroundColor": "#121212",
            "borderRadius": "10px",
            "boxShadow": "0 0 8px #00ff99",
            "color": "#f2f2f2",
        }
    ),

    html.Div(
        id='player-summary-container',
        style={
            "display": "flex",
            "justifyContent": "space-around",
            "margin": "40px"
        }
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


# Callbacks.
from dash import ctx, ALL  # This is important in newer Dash versions

@app.callback(
    Output('clicked-player', 'data'),
    Input({'type': 'player-card', 'index': ALL}, 'n_clicks'),
)
def store_clicked_player(n_clicks_list):
    # Find which button was clicked (value > 0)
    triggered = ctx.triggered_id
    if not triggered:
        return dash.no_update

    return triggered['index']

@app.callback(
    Output('trend-graph', 'figure'),
    Input('player-dropdown', 'value')
)
def update_graph(selected_players):
    if not selected_players:
        return px.line(title="No players selected.")

    fig = px.line(
        df[selected_players],
        labels={"value": "Popularity", "index": "Date"},
        title="Google Search Trends (Last 3 Months)",
        color_discrete_map={
            "Mohamed Salah": "#e60000",
            "Achraf Hakimi": "#0055ff",
            "Ismaila Sarr": "#00b894",
            "Kamaldeen Sulemana": "#e67e22",
            "Carlos Baleba": "#f1c40f",
            "Bryan Mbuemo": "#9b59b6",
            "Samuel Chukweze": "#1abc9c",
            "Antoine Semenyo": "#2980b9",
            "Ademola Lookman": "#c0392b",
            "Serhou Guirassy": "#2ecc71",
            "Bilal El Khannouss": "#d35400",
            "Mohammed Kudus": "#8e44ad",
            "Ilaix Moriba": "#34495e"
        },
        template="plotly_dark"
    )

    # Custom hover text with avatars
    for trace in fig.data:
        player = trace.name
        avatar_path = f"/assets/avatars/{player.lower().replace(' ', '_')}.jpg"

        trace.hovertemplate = (
            f"<b>{player}</b><br>" +
            "Date: %{x}<br>" +
            "Popularity: %{y}<br><br>" +
            f"<img src='{avatar_path}' style='width:40px;height:40px;border-radius:50%;'><extra></extra>"
        )
        trace.mode = "lines+markers"
        trace.line.width = 3

    fig.update_layout(
        plot_bgcolor="#1c1c1c",
        paper_bgcolor="#1c1c1c",
        font=dict(color="#f2f2f2"),
        title_font_size=24,
        legend=dict(
            bgcolor="#1c1c1c",
            bordercolor="gray",
            borderwidth=1
        ),
        legend_title_text="Players"
    )

    return fig

@app.callback(
    Output('trending-player-card', 'children'),
    Input('player-dropdown', 'value')
)
def update_trending_card(selected_players):
    if not selected_players:
        return html.Div("No players selected")

    # Calculate weekly change
    last_7 = df[selected_players].tail(7).mean()
    prev_7 = df[selected_players].iloc[-14:-7].mean()
    change = ((last_7 - prev_7) / prev_7) * 100

    trending_player = change.idxmax()
    trend_value = round(change.max(), 2)
    avatar_path = f"/assets/avatars/{trending_player.lower().replace(' ', '_')}.jpg"

    return html.Div([
        html.Img(src=avatar_path, style={
            "width": "80px", "height": "80px", "borderRadius": "50%", "marginBottom": "10px"
        }),
        html.H3(f"{trending_player}", style={"margin": "5px 0", "color": "#00ff99"}),
        html.P(f"🔥 Popularity up {trend_value}% this week!", style={"fontSize": "16px"})
    ], style={
        "backgroundColor": "#1e1e1e",
        "padding": "20px",
        "borderRadius": "10px",
        "boxShadow": "0 0 10px #00ff99",
        "textAlign": "center",
        "width": "250px",
        "margin": "auto"
    }, className="trending-animate")

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

@app.callback(
    Output('fan-buzz', 'children'),
    Input('player-dropdown', 'value')
)
def update_fan_buzz(selected_players):
    if not selected_players:
        return html.Div("No players selected")

    # Mock buzz data (simulate real-time headlines)
    fake_buzz = [
        "🗣 Salah’s Champions League form is back in the news",
        "🔥 Kamaldeen’s sprint clip goes viral on TikTok",
        "🎯 Kudus leads search spikes after Man of the Match display",
        "🇲🇦 Hakimi’s recovery stats spark debate online",
        "💥 Lookman’s free kick trending in Nigeria & UK"
    ]

    return html.Ul([
        html.Li(buzz, style={"marginBottom": "10px"}) for buzz in fake_buzz
    ])

@app.callback(
    Output('leaderboard-container', 'children'),
    Input('player-dropdown', 'value')
)
def update_leaderboard(selected_players):
    if not selected_players:
        return html.Div("No players selected", style={"color": "#888"})

    # Filtering last 7 days of data.
    recent_df = df.tail(7)  # or use df[df['date'] > (today - timedelta)]

    # Computing average score for each selected player.
    scores = {
        player: round(recent_df[player].mean(), 1)
        for player in selected_players if player in recent_df.columns
    }

    # Sorting and getting top 5.
    top_players = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]

    # Creating leaderboard cards.
    cards = []
    for i, (player, score) in enumerate(top_players, start=1):
        avatar_path = f"/assets/avatars/{player.lower().replace(' ', '_')}.jpg"
        cards.append(html.Div([
            html.Img(src=avatar_path, style={
                "width": "50px", "height": "50px", "borderRadius": "50%", "marginRight": "10px"
            }),
            html.Div([
                html.H4(f"{i}. {player}", style={"margin": 0}),
                html.P(f"🔥 {score}/100", style={"margin": 0, "fontSize": "14px", "color": "#00ff99"})
            ])
        ], style={
            "display": "flex",
            "alignItems": "center",
            "backgroundColor": "#1e1e1e",
            "padding": "10px 15px",
            "borderRadius": "8px",
            "marginRight": "10px",
            "boxShadow": "0 0 5px #00ff99"
        }))

    return html.Div(cards, style={
        "display": "flex",
        "overflowX": "auto",
        "gap": "15px"
    })

@app.callback(
    Output('player-info-container', 'children'),
    Input('player-dropdown', 'value'),
    Input('clicked-player', 'data'),
)
def update_player_info(selected_players, clicked_player):
    if not selected_players:
        return html.Div("Select a player to see their profile", style={"color": "#888"})

    cards = []
    for player in selected_players:
        info = player_metadata.get(player)
        if not info:
            continue

        # getting avatar path.
        avatar_path = f"/assets/avatars/{player.lower().replace(' ', '_')}.jpg"

        # checking if this player was clicked(to expand their card).
        is_expanded = (clicked_player == player)

        # Base layout of the player card.
        base_card = html.Div([
            html.Img(src=avatar_path,
                     style={
                       "width": "70px",
                       "height": "70px",
                       "borderRadius": "50%",
                       "marginBottom": "10px"
                    }
            ),
            html.H3(player),
            html.P(f"Club: {info['club']}"),
            html.P(f"Country: {info['country']}"),
            html.P(f"Position: {info['position']}"),
        ])

        # Extra section only shown if player was clicked.
        expanded_section = None
        if is_expanded:
            expanded_section = html.Div([
                html.Hr(style={"borderTop": "1px solid #555"}),
                html.P(info['bio'], style={"fontStyle": "italic", "color": "#aaa"}),

                html.Iframe(
                    src=info.get("youtube_url"),
                    width="100%",
                    height="180",
                    style={
                        "border": "none",
                        "marginTop": "10px",
                        "borderRadius": "6px",
                    }
                )
            ],
            className="expanded",
            style={"maxHeight": "0"})

        # wrapping the base card and expanded section inside a button.
        cards.append(html.Button(
            html.Div([base_card, expanded_section], style={
                "textAlign": "center",
                "padding": "10px",
                "backgroundColor": "#1c1c1c",
                "borderRadius": "8px",
                "width": "220px",
                "boxShadow": "0 0 5px #00ff99",
                "marginRight": "20px",
        }),
            id={'type': 'player-card', 'index': player},
            n_clicks=0,
            style={"border": "none", "background": "none", "padding": 0, "cursor": "pointer"}
        ))

    return html.Div(cards, style={
        "display": "flex",
        "flexWrap": "wrap",
        "gap": "20px"
    })

# Run.
if __name__ == "__main__":
    app.run(debug=True)