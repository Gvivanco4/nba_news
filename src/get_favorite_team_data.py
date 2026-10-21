import data_ingestion as data
from llm_client import ai_caller
import pandas as pd

FAVORITE_TEAMS = ["Lakers", "Mavericks", "Spurs", "Timberwolves", "Knicks"]

def filter_games_transactions_fav_teams():
    games = data.get_today_games()
    transactions = data.get_transactions()
    
    filtered_games = [game for game in games if game["team_1"] in FAVORITE_TEAMS or game["team_2"] in FAVORITE_TEAMS]
    filtered_transactions = [t for t in transactions if t["team"].title() in FAVORITE_TEAMS][:10]

    return filtered_games, filtered_transactions


def filter_relevant_news():
    filtered_news = ai_caller.prompt_ai(data.get_news())
    return filtered_news

def rank_player_stats():
    stats = data.get_stats()
    stats_table = pd.DataFrame(stats)
    if stats_table.empty:
        return []
    numeric_stats = pd.to_numeric(stats_table["stat"], errors="raise")
    stats_table["rank"] = numeric_stats.groupby(stats_table["category"]).rank(
        ascending=False, method="min"
    ).astype(int)
    final = stats_table.to_dict(orient="records")
    return final






