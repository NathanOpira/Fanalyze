# Fanalyze

*Fanalyze* is a global-facing sports analytics dashboard focused on tracking and visualizing the online popularity of African football stars.

Built with Python and Plotly Dash, it offers real-time insights into how players are trending digitally — starting with Google Trends data, with plans to expand into platforms like TikTok, Instagram, and news media.

---

## 🌍 MVP Scope

### 🎯 Tracked Players
- Elias Moriba
- Kamaldeen Suleimana
- Carlos Baleba
- Bryan Mbuemo
- Ismaila Sarr
- Mohamed Salah
- Samuel Chukwueze
- Antoine Semenyo
- Achraf Hakimi
- Ademola Lookman
- Serhou Guirassy
- Bilal El Khannouss
- Mohammed Kudus

### 📊 Data Sources
- ✅ Google Trends (live and historical interest)
- 🟡 TikTok (under research for API/scraping access)

---

## 🛠 Tech Stack

- Python (pandas, pytrends)
- Plotly Dash (dashboard)
- Vercel (deployment)
- [Future Add-ons: TikTok API, sentiment analysis, YouTube mentions]

---

## 📁 Project Structure

```bash
fanalyze/
├── data/
│   ├── raw/                # Unprocessed Google Trends data
│   └── processed/          # Cleaned data for dashboard
├── notebooks/              # Jupyter notebooks for exploration
├── src/
│   ├── fetch_trends.py     # Pulls Google Trends data
│   ├── clean_data.py       # Cleans and normalizes trend data
│   ├── dash_app.py         # Dash dashboard app
│   └── utils.py            # Helper functions
├── assets/                 # Images, CSS, logos
├── README.md
├── requirements.txt
├── .gitignore
└── vercel.json

Built by @NathanOpira
Powered by Python and passion for sports tech in Africa and beyond.