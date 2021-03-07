all_bets = []
with open('valuebets07.03.2021.txt', 'r') as file:
    [all_bets.append(line) for line in file.readlines()]

for game in all_bets:
    value_token = game.split('-> Value:')[1].split('|')[0]
    value = float(value_token.strip())
    if value > 7.50:
        print(game)