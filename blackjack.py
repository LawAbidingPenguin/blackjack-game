import random
import time

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

class Card:

    def __init__(self,suit,rank):

        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:

    def __init__(self):
        
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit,rank))

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop()

class Player:

    def __init__(self,bankroll=1000):

        self.hand = []
        self.bankroll = bankroll
    
    def place_bet(self):

        bet = input("Place a bet: ")
        # Checking if bet places is numeric and therefore valid
        while bet.isnumeric() == False:

            bet = input("Invalid bet, try again...")

            if bet.isnumeric() == True:
                break
        
        bet = int(bet)
        
        # Checking if bet isn't bigger than the bankroll
        while bet > self.bankroll:

            bet = int(input("Insufficient funds to place bet, try again: "))

            if bet <= self.bankroll:
                break        
        
        self.bankroll -= bet
        return bet

    def hit(self,new_card):
        self.hand.append(new_card)

    def show_hand(self):
        for x in self.hand:
            print(x)

class Dealer:

    def __init__(self):

        self.hand = []

    def hit(self,new_card):
        self.hand.append(new_card)

    def show_hand(self):
        for x in self.hand:
            print(x)

# Welcoming message and showing the rules
print("--- WELCOME TO BLACKJACK ---\n")
print("Rules: \n-The goal of blackjack is to beat the dealer's hand without going over 21.\n-Face cards are worth 10. Aces are worth 1 or 11, whichever makes a better hand.")
print("-Round starts by placing a bet, you need at least $1 to place a bet...")
print("-Each player starts with two cards, one of the dealer's cards is hidden until the end.\n-To 'Hit' is to ask for another card. To 'Stand' is to hold your total and end your turn.")
print("-If you go over 21 you bust, and the dealer wins regardless of the dealer's hand.\n-If you are dealt 21 from the start (Ace & 10), you got a blackjack.")
print("-Dealer will hit until his/her cards total 17 or higher.")
print("-Press Ctrl + C at any time to cash out and leave the table...\n")

start = input("--- Press Enter to start ---")


new_player = Player()
new_dealer = Dealer()

game_on = True
while game_on:

    new_deck = Deck()
    new_deck.shuffle()

    # Using round_not_over to determine if round is over during player's or dealer's turn
    # If not, proceed to final check...
    round_not_over = True
    player_turn = True
    dealer_turn = True

    new_player.hand = []
    new_dealer.hand = []

    if new_player.bankroll < 1:
        print("Out of funds, cannot place bet. YOU LOSE!!!")
        game_on = False
        break

    for x in range(2):
        new_player.hit(new_deck.deal_one())
        new_dealer.hit(new_deck.deal_one())

    print("\n\n")
    print("New Round...")
    print(f"Bankroll: ${new_player.bankroll}")
    bet = new_player.place_bet()
    earnings = bet * 1.5

    print("\n--- Player hand --- ")
    new_player.show_hand()
    
    print("\n--- Dealer hand (one card hidden) --- ")
    print(new_dealer.hand[0], "\n")

    # Player Turn Loop
    while player_turn:

        # Player_hand_value is the values of all the cards in the player's hand
        # Player_hand_sum is the total sum of all the values
        player_hand_values = []
        for x in new_player.hand:
            player_hand_values.append(values[x.rank])
        player_hand_sum = sum(player_hand_values)

        # Check for Ace and adjust player_hand_sum
        if player_hand_sum > 21 and 11 in player_hand_values:
            player_hand_sum -= 10
        
        # Checking to see if player has BUST or BLACKJACK
        if player_hand_sum == 21:
            print("\n\n")
            print(f"Round won! Earnings: ${earnings}")
            new_player.bankroll += earnings
            round_not_over = False
            dealer_turn = False
            player_turn = False
            break
        elif player_hand_sum > 21:
            print("\n\n")
            print(f"Round lost! You lost ${bet}")
            round_not_over = False
            dealer_turn = False
            player_turn = False
            break

        # Creating a While Loop to ask the user to Hit or Stand
        hit_stand = "WRONG"
        while hit_stand != 'S':

            while hit_stand not in ["H","S"]:
                hit_stand = input("Enter 'H' to Hit and 'S' to stand: ").upper()

                if hit_stand not in ["H","S"]:
                    print("Wrong input, try again...")
                    hit_stand = input("Enter 'H' to Hit and 'S' to stand: ").upper()

            if hit_stand == "H":
                new_player.hit(new_deck.deal_one())

                print("\n\n\n\n")
                print("\n--- Player hand ---")
                new_player.show_hand()
                
                print("\n---Dealer hand (one card hidden) --- ")
                print(new_dealer.hand[0], "\n")

                break
            else:
                hit_stand = 'S'
                player_turn = False
                break

    # Dealer Turn Loop
    while dealer_turn:
        print("\n--- Dealer's Turn ---")

        dealer_hand_values = []
        for x in new_dealer.hand:
            dealer_hand_values.append(values[x.rank])
        dealer_hand_sum = sum(dealer_hand_values)

        # Dealer keeps receing new cards until dealer_hand_sum < 17
        if dealer_hand_sum < 17:
            new_dealer.hit(new_deck.deal_one())

        # Adding time.sleep so dealer's turn won't be instant
        time.sleep(1)
        print("...")
        time.sleep(1)
        print("...")
        time.sleep(1)
        print("...")

        print("\n\n")
        print("\n--- Player hand ---")
        new_player.show_hand()
        
        print("\n---Dealer hand --- ")
        new_dealer.show_hand()
        
        # Check for Ace and adjust dealer_hand_sum
        if dealer_hand_sum > 21 and 11 in dealer_hand_values:
            dealer_hand_sum -= 10

        if dealer_hand_sum == 21:
            print("\n\n")
            print(f"DEALER WINS! You lose ${bet}")
            round_not_over = False
            dealer_turn = False
            break
        elif dealer_hand_sum > 21:
            print("\n\n")
            print(f"DEALER BUST! You win {earnings}")
            new_player.bankroll += earnings

            round_not_over = False
            dealer_turn = False
            break

        if dealer_hand_sum >= 17:
            round_not_over = True
            dealer_turn = False
        
        # Check for Ace and adjust dealer_hand_sum
        if dealer_hand_sum > 21 and 11 in dealer_hand_values:
            dealer_hand_sum -= 10
    
    # Final check to determine round winner...
    if round_not_over == True:
        if dealer_hand_sum in range(17,21):
            if player_hand_sum > dealer_hand_sum:
                print("\n\n")
                print(f"YOU WIN! Earnings: ${earnings}")
                new_player.bankroll += earnings
                continue
            elif dealer_hand_sum > player_hand_sum:
                print("\n\n")
                print(f"DEALER WINS! You have lost: ${bet}")
                continue
            else:
                print("\n\n")
                print(f"IT IS A DRAW! Bet returned to bankroll...")
                new_player.bankroll += bet
                continue

        