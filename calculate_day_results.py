all_bets = []
with open('valuebets06.03.2021.txt', 'r') as file:
    [all_bets.append(line) for line in file.readlines()]

# print(all_bets)
total_profit = 0
for game in all_bets:
    value_token = game.split('-> Value:')[1].split('|')[0]
    value = float(value_token.strip())
    # print(value)
    if value > 10:
        try:
            profit_token = game.split('|')[1]
            plus_minus = profit_token.split(' ')[1]
            amount = profit_token.split(' ')[2].replace('\n', '')
            # print(profit_token.split(' '))
            if plus_minus == '-':
                total_profit -= float(amount)
            else:
                total_profit += float(amount)
            print(total_profit)
        except:
            pass
# print(total_profit)