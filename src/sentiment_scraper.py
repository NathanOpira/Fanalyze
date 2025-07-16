import snscrape.modules.twitter as sntwitter
import re
from collections import Counter

def fetch_recent_tweets(player_name, max_tweets=50):
    tweets = []
    query = f'"{player_name}" lang:en'  
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= max_tweets:
            break
        tweets.append(tweet.content)
    return tweets

def extract_keywords(tweets):
    all_words = []
    for tweet in tweets:
        # Clean tweet text
        clean = re.sub(r"http\S+|@\S+|#\S[^A-Za-z\s]", "", tweet.lower())
        words = clean.split()
        all_words.extend([w for w in words if len(w) > 2])  # Filter out short words.
    # Get top 50 most frequent words.
    common_words = [w for w, _ in Counter(all_words).most_common(50)]
    return common_words