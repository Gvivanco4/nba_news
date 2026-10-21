from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape

from get_favorite_team_data import (
    filter_games_transactions_fav_teams,
    filter_relevant_news,
    rank_player_stats,
)
from send_email import send_email

def main():
    games, transactions = filter_games_transactions_fav_teams()
    news = filter_relevant_news()
    stats = rank_player_stats()
    today = datetime.now(ZoneInfo("America/Mexico_City")).date()

    env = Environment(
        loader=FileSystemLoader(Path(__file__).resolve().parent / "templates"),
        autoescape=select_autoescape(["html", "xml"]),
        undefined=StrictUndefined,
    )
    template = env.get_template("newsletter.html")
    html = template.render(
        games=games,
        transactions=transactions,
        stats=stats,
        news=news,
        date=today.strftime("%d/%m/%Y"),
    )

    send_email(html, subject=f"NBA Daily News {today}")
    print("Newsletter enviado correctamente.")


if __name__ == "__main__":
    main()
