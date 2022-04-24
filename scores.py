# Print Live Games
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
