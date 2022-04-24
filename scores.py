import requests
import pandas
import json
from dateutil import parser
from pytz import timezone
import pytz

## Taken from ESPN Curl, Imported into Insomnia, Pasted Generated Python below
url = "https://site.web.api.espn.com/apis/v2/scoreboard/header"

querystring = {"sport":"baseball","league":"mlb","region":"us","lang":"en","contentorigin":"espn","buyWindow":"1m","showAirings":"buy,live,replay","showZipLookup":"true","tz":"America/New_York"}

payload = ""
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Origin": "https://www.espn.com",
    "Connection": "keep-alive",
    "Referer": "https://www.espn.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "TE": "trailers"
}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
response = json.loads(response.text)

# Dependencies
list_games = response['sports'][0]['leagues'][0]['events'][0:]
num_games = len(list_games)
games_final = []
games_live = []
games_scheduled = []
games_delayed = []

## For Loop to find each game
for x in range(num_games):
    game = response['sports'][0]['leagues'][0]['events'][x]

    
    ## Dependencies
    teams_list = game['competitors']
    time_raw = (parser.parse(game['date'])).astimezone(timezone('US/Pacific'))
    time_format='%H:%M %p'

    # # Team 1 Info
    home_abv = teams_list[0]['abbreviation'] # SEA
    home_mascot = teams_list[0]['name'] # Mariners
    home_city = teams_list[0]['location'] # Seattle
    home_score = teams_list[0]['score']
    home_record = teams_list[0]['record'] # 13-2
    home_abv_cen = home_abv + '  : ' if len(home_abv)< 3 else home_abv + ' : '
    home_abv_spc = home_abv + '  ' if len(home_abv)< 3 else home_abv + ' '
    home_abv_win = '*' + home_abv + ' : ' if len(home_abv)< 3 else '*' + home_abv + ': '

    # # Team 2 Info
    away_abv = teams_list[1]['abbreviation']
    away_mascot = teams_list[1]['name']
    away_city = teams_list[1]['location']
    away_score = teams_list[1]['score']
    away_record = teams_list[1]['record']
    away_abv_cen = away_abv + '  : ' if len(away_abv)< 3 else away_abv + ' : '
    away_abv_spc = away_abv + '  ' if len(away_abv)< 3 else away_abv + ' '
    away_abv_win = '*' + away_abv + ' : ' if len(away_abv)< 3 else '*' + away_abv + ': '

    location = game['location']# Arena
    time = time_raw.strftime(time_format)# 10:10 AM

    inning = game['period']
    inning_prefix = game['fullStatus']['periodPrefix'][0:3]# top/bottom
    inning_sum = inning_prefix + f' {str(inning)}'# Top 1 
    inning_sum_cen = '  '+inning_sum

    try:
        outs = str(game['outsText'][0:])
    except KeyError:
        outs = 'Final'
    outs_sum_cen = '  '+ outs

    home_odds = game['odds']['home']['moneyLine']
    away_odds = game['odds']['away']['moneyLine']

    fav = 'home' if home_odds < away_odds else 'away'
    fav_team = home_abv if fav == 'home' else away_abv
    fav_odds = f'({home_odds})' if fav == 'home' else f'({away_odds})'
    fav_sum = f'FAV: {fav_team} {fav_odds}'

    try:
        winning_team = 'Home' if int(home_score) > int(away_score) else 'Tie' if int(home_score) == int(away_score) else 'Away'
    except ValueError:
        winning_team = False
    batting_abv = home_abv if inning_prefix.lower() == 'bot' else away_abv
    batting_sum = batting_abv + ' at bat'# TB at bat
    batting_sum_cen = f'   {batting_sum}   '

    status = 'Final' if game['status'] == 'post' else 'Live' if game['status'] == 'in' else 'Scheduled'
    delay = True if game['wasSuspended'] == 'True' else False
    delay_sum = 'Game Delay' if delay == True else 'No Delay'
    extra_innings = True if inning > 9 else False

    try:
        base_1 = True if game['onFirst'] > 0 else False
        base_2 = True if game['onSecond'] > 0 else False
        base_3 = True if game['onThird'] > 0 else False
        base_sum = game['baseRunnersText']
        base_sum_team = batting_abv + f'- {base_sum}'
    except KeyError:
        pass
    # Display Dependencies
    b1 = 'X' if base_1 == True else ' '
    b2 = 'X' if base_2 == True else ' '
    b3 = 'X' if base_3 == True else ' '

    base_array= f'   [{b2}]   \n[{b3}] o [{b1}]\n   [ ]   '
    base_array_cen = f'      [{b2}]   \n   [{b3}] o [{b1}]\n      [ ]   '

    line = '---------'
    star = '   ***   '

    #live display
    display_live = f'{star}\n{line}\n{inning_sum_cen}\n{away_abv_cen}{away_score}\n{home_abv_cen}{home_score}\n{line}\n{base_array}\n{outs_sum_cen}\n{line}\n{base_sum_team}\n{line}'

    #final display
    home_abv_cen = home_abv_win if winning_team == 'Home' else home_abv_cen
    away_abv_cen = away_abv_win if winning_team == 'Away' else away_abv_cen
    display_final = f'{star}\n{line}\nFinal\n{away_abv_cen}{away_score}\n{home_abv_cen}{home_score}\n{line}\n{away_abv_spc}({away_record})\n{home_abv_spc}({home_record})\n{line}'

    #scheduled display
    display_scheduled = f'{star}\n{line}\nToday @ {time}\n{away_abv_spc}({away_record})\n{home_abv_spc}({home_record})\n{line}\n{location}\n{fav_sum}\n{line}'

    #delay display
    display_delay = f'{star}\n{line}\n**Delay**\n{away_abv_cen}{away_score}\n{home_abv_cen}{home_score}\n{line}\n{inning_sum} | {outs}\n{location}\n{line}'

    if delay == True:
        games_delayed.append(display_delay)
    elif status == 'Final':
        games_final.append(display_final)
    elif status == 'Live':
        games_live.append(display_live)
    else:
        games_scheduled.append(display_scheduled)

## Output Games
# If present- print games with description
if len(games_delayed) > 0:
    print(f'- {len(games_delayed)} LIVE -')
    for game in range(len(games_delayed)):
        print(f'{games_delayed[game]}\n')
    print(f'\n\n\n')
if len(games_live) > 0:
    print(f'- {len(games_live)} LIVE -')
    for game in range(len(games_live)):
        print(f'{games_live[game]}\n')
    print(f'\n\n\n')
if len(games_final) > 0:
    print(f'- {len(games_final)} FINAL -')
    for game in range(len(games_final)):
        print(f'{games_final[game]}\n')
    print(f'\n\n\n')
if len(games_scheduled) > 0:
    print(f'- {len(games_scheduled)} COMING UP -')
    for game in range(len(games_scheduled)):
        print(f'{games_scheduled[game]}\n')
