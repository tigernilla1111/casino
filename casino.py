# bacarat outcome has winner tie natural is_big
import bacarat

outcome_dic = {"B": "banker", "P": "player", "T": "tie"}
game = bacarat.Game()
stats = open("stats.txt", "r")
#money = int(stats.readline())
money = 1000
stats.close()
stats = open("stats.txt", "w")

class Bet:
    def __init__(self, bet_input):
        parse = bet_input.split()
        self.placement = parse[1].lower()
        self.amount = int(parse[0])
    def print(self):
        print(self.amount, " on ", self.placement)

def bacarat_outcome_check(bets, outcome):
    gain = 0
    # Go through bets and see which ones hit
    for b in bets:
        if b.placement == outcome_dic[outcome.winner]:
            if outcome.winner == "T":
                gain += b.amount * 9
            else:
                gain += b.amount * 2
        if b.placement == "big" and outcome.is_big:
            gain += b.amount * 1.5
        elif b.placement == "small" and not outcome.is_big:
            gain += b.amount * 2.5
        if b.placement in ["player", "banker"] and outcome.tie:
            gain += b.amount
    return gain

prev_bets = []
prev_total_bet = 0
for i in range(30):
    bets = []
    total_bet_amount = 0
    while((bet_input := input("amount and on what (e.g. 10 small) then type go: ")) != "go"):
        # User types in "r" to easily rebet and go 
        if bet_input=="r":
            bets = prev_bets
            for b in bets:
                b.print()
            print("")
            total_bet_amount = prev_total_bet
            break

        # Construct bet object from user input
        bet = Bet(bet_input)
        total_bet_amount += bet.amount
        bets.append(bet)
    print("")
    money -= total_bet_amount
    outcome = game.play_round()
    outcome.print()
    gain = bacarat_outcome_check(bets, outcome)
    if gain > 0:
        print("\nYou won $" + str(gain))
    money += gain
    stats.write(str(money))
    print("\n\n\n")
    print("You have $" + str(money))
    prev_bets = bets.copy()
    prev_total_bet = total_bet_amount
stats.close()



