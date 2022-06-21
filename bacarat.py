from deck_of_cards import deck_of_cards
from colorama import init, Fore, Back, Style
import time

CARDS_LEFT_WHEN_SHUFFLE = 15
NUM_DECKS = 6

class Outcome:
    def __init__(self, player_points, banker_points, natural=False, is_big=True):
        if player_points == banker_points:
            self.winner = "T"
            self.tie = True
            self.winning_score = player_points
        elif player_points<banker_points:
            self.winner = "B"
            self.tie = False
            self.winning_score = banker_points
        else:
            self.tie = False
            self.winner = "P"
            self.winning_score = player_points
        self.natural = natural
        self.is_big = is_big
    def print(self):
        if self.tie:
            print("TIE", end = "")
        else:
            print(self.winner, end = "")
        print(" with", self.winning_score, end = "")
        if self.is_big:
            print("   BIG", end = "")
        else:
            print("   SMALL", end = "")
        if self.natural:
            print("   NATURAL")

def deck_shuffle():
    # Empty out shoe
    deck_obj = deck_of_cards.DeckOfCards()
    while len(deck_obj.deck) != 0:
        deck_obj.deck.pop()
    
    for i in range(NUM_DECKS):
        deck_obj.add_deck()
    deck_obj.shuffle_deck()
    return deck_obj


def deal_cards(DECK, is_game):
    #player banker player banker deal order
    player_hand = []
    banker_hand = []
    for i in range(2):
        player_hand.append(DECK.deck.pop())
        banker_hand.append(DECK.deck.pop())

    player_points = hand_value(player_hand)
    banker_points = hand_value(banker_hand)
    if is_game:
        print_hands(player_hand, player_points, banker_hand, banker_points)
    
    #if both the player and banker have 6 or 7 points, no third card is drawn
    if banker_points in [6, 7] and player_points in [6, 7]:
        return Outcome(player_points, banker_points, is_big=False)
    
    #if either the banker or player have 8 or 9 points, game is over as a natural
    if is_natural(banker_points) or is_natural(player_points):
        return Outcome(player_points, banker_points, natural=True, is_big=False)

    # If the player hand has a total of from zero to five, then a third card is dealt to that hand.
    extra_player = None
    if 0 <= player_points <= 5:
        extra_player = DECK.deck.pop()
        player_hand.append(extra_player)
        player_points = hand_value(player_hand)
    
    
    # if the Player hand has not been dealt a third card, then the above rule applies to the Banker hand;
    if extra_player is None and 0 <= banker_points <= 5:
        banker_hand.append( DECK.deck.pop())
        banker_points = hand_value(banker_hand)
    # In the case where a third card was dealt to the Player hand, then the following table applies;
    elif extra_player is not None:
        if (extra_player.rank==2 or extra_player.rank==3) and 0<=banker_points<=4:
            banker_hand.append(DECK.deck.pop())
        elif (extra_player.rank==4 or extra_player.rank==5) and 0<=banker_points<=5:
            banker_hand.append(DECK.deck.pop())
        elif (extra_player.rank==6 or extra_player.rank==7) and 0<=banker_points<=6:
            banker_hand.append(DECK.deck.pop()) 
        elif extra_player.rank==8 and 0<=banker_points<=2:
            banker_hand.append(DECK.deck.pop())
        elif (extra_player.rank==1 or extra_player.rank>=9) and 0<=banker_points<=3:
            banker_hand.append(DECK.deck.pop())
        banker_points = hand_value(banker_hand)

    banker_points = hand_value(banker_hand)
    player_points = hand_value(player_hand)
    if is_game:
        time.sleep(2)
        print_hands(player_hand, player_points, banker_hand, banker_points)
        print("")

    return Outcome(player_points, banker_points, is_big= not(len(player_hand) == 2 and len(banker_hand) == 2))




def is_natural(points):
    if points == 8 or points == 9:
        return True
    return False


def hand_value(hand):
    value = 0 
    for card in hand:
        if card.rank not in [10, 11, 12, 13]:
            value += card.rank
    return value % 10 

def print_hands(player_hand, player_points, banker_hand, banker_points):
    is_last_print = False
    if ((banker_points in [6, 7] and player_points in [6,7]) or player_points in [8, 9] or banker_points in [8,9]):
        is_last_print = True
    divider = " " * 25
    if(len(player_hand) == 3):
        cumu = Back.BLUE + "  ||"
        for card in player_hand:
            cumu += ("  " + card.name + "  ||")
        # Change divider so banker hand is displayed in the same spot
        # when player gets an extra card  
        divider = " " * (25- (len(player_hand[2].name) + 6))
        cumu += (Style.RESET_ALL + divider + Back.RED + "  ||")
        for i in range(len(banker_hand)):
            cumu += ("  " + banker_hand[i].name + "  ||")
            if i == 1:
                print(cumu, Style.RESET_ALL, end = "\r")
        time.sleep(1)
        print(cumu, Style.RESET_ALL)
        time.sleep(2)
    else:
        print_order = player_hand +  banker_hand
        cumu = Back.BLUE + "  ||"
        for card in player_hand:
            cumu += ("  " + card.name + "  ||") 
            print(cumu, end = "\r")
            time.sleep(1)
        cumu += (Style.RESET_ALL + divider + Back.RED + "  ||")
        for card in banker_hand:
            cumu += ("  " + card.name + "  ||") 
            print(cumu, Style.RESET_ALL, end = "\r")
            time.sleep(1)
        if is_last_print:
            print(cumu, Style.RESET_ALL)


class Game:
    def __init__(self):
        self.deck_obj = deck_shuffle()

    def run_shoe(self):
        outcomes = {"B": 0, "P": 0, "T": 0, "BIG": 0, "SMALL": 0}
        while len(self.deck_obj.deck) > CARDS_LEFT_WHEN_SHUFFLE:
            outcome = deal_cards(self.deck_obj, False)
            outcomes[outcome.winner] += 1
            if outcome.is_big:
                outcomes["BIG"] += 1
            else:
                outcomes["SMALL"] += 1

            
        self.deck_obj = deck_shuffle()
        return outcomes

    def play_round(self):
        init()
        if len(self.deck_obj.deck) <= CARDS_LEFT_WHEN_SHUFFLE:
            self.deck_obj = deck_shuffle()
        outcome = deal_cards(self.deck_obj, True)
        print("Cards left: " + str(len(self.deck_obj.deck)))
        return outcome
