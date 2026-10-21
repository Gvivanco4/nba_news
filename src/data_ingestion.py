import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36'}

def get_transactions():

    nba_url = "https://stats.nba.com/js/data/playermovement/NBA_Player_Movement.json"

    response = requests.get(nba_url, headers=headers)
    response.raise_for_status()

    data = response.json()
    json = [{"team": description["TEAM_SLUG"], "description": description["TRANSACTION_DESCRIPTION"]} for description in data["NBA_Player_Movement"]["rows"] ]
    return json

def get_news():
    nba_news_url = "https://www.nba.com/news"
    

    response = requests.get(nba_news_url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    elements = soup.find_all(class_="MultiLineEllipsis_ellipsis__mpkNo")
    json = [
        {"title": elements[i].get_text(), 
         "description": elements[i + 1].get_text() 
         }
         for i in range(0, len(elements) - 1, 2)
    ]
    return json

def get_today_games():
    games_url = "https://www.nba.com/games"
    response = requests.get(games_url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    elements = soup.find_all(class_="MatchupCardTeamName_teamName__0cu0j")
    game_time = soup.find_all(class_="GameCardMatchupStatusText_gcsText__L1K1e")

    json = [{
        "team_1": elements[i].get_text(),
        "team_2": elements[i + 1].get_text(),
    }
        for i in range(0, len(elements) - 1, 2)
    ]

    for i in range(0, len(json), 1):
        json[i]["game_time"] = game_time[i].get_text()

    return json

def get_stats():
    stats_url = "https://www.nba.com/stats/players"
    response = requests.get(stats_url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    players = [
    e.get_text()
    for e in soup.select(
        ".Anchor_anchor__wnmj2.LeaderBoardPlayerCard_lbpcTableLink__Gu2tH, "
        ".players_cardValue__ihPhs"
    )
]    

    core_stats_players = players[:60]
    json = [
        {
            "player": core_stats_players[i],
            "stat": core_stats_players[i + 1]
        }
        for i in range(0, len(core_stats_players) - 1, 2)
    ]

    
    for i in range(0, len(json), 1):
        if i <= 4:
            json[i]["category"] = "points"
        elif i >= 5 and i < 10:
            json[i]["category"] = "rebounds"
        elif i >= 10 and i < 15:
                    json[i]["category"] = "assist"
        elif i >= 15 and i < 20:
                    json[i]["category"] = "blocks"
        elif i >= 20 and i < 25:
                    json[i]["category"] = "steals"
        elif i >= 25 and i < 30:
                    json[i]["category"] = "field_goal_per"

    return json





    







