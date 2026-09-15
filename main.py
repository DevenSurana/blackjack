# Blackjack
# 9/3/26
__author__ = "Deven Surana"


# libraries
import random


# variables and lists
# variables and lists
suits = ["♠", "♥", "♦", "♣"]
numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

deck = []

player_hand = []
player_hand_2 = []
dealer_hand = []

money = 1000
amount_bet = 0
amount_bet_2 = 0

is_player_turn = True

dealing_playerhand_1 = True

compare_count = 0

playing = True
has_split = False

# functions
def shuffle(suit, number):
    for i in range(0, 6):
        for number in numbers:
            for suit in suits:
                deck.append(number+suit)

    random.shuffle(deck)

    
def get_card_value(card):
    value = card[:-1]

    if value in ["J", "Q", "K"]:
        return 10
    elif value == "A":
        return 11
    else:
        return int(value)


def check_split(hand):
    if get_card_value(hand[0]) == get_card_value(hand[1]):
        return True
    else:
        return False

def split():
    global has_split
    global money
    global amount_bet
    global amount_bet_2

    if len(player_hand) == 2 and check_split(player_hand) and has_split == False:
        print("Your hand:", *player_hand)
        print("Total value:", get_hand_value(player_hand))
        print("\nDealer hand:", dealer_hand[0], "XX \n")
        action = input("Do you want to split (hit/stand later)? (y/n): ")

        if action.lower() == "y":
            player_hand_2.append(player_hand.pop(1))
            amount_bet_2 = amount_bet

            print("Hand 1:", *player_hand)
            print("Amount Bet:", amount_bet)
            print("Hand 2:", *player_hand_2)
            print("Amount Bet:", amount_bet_2)
            print()
            print("Dealing extra card to each hand")
            pick_random_card(player_hand)
            pick_random_card(player_hand_2)

            print("Hand 1:", *player_hand)
            print("Hand 2:", *player_hand_2)
            print("\n")

            has_split = True


def try_again():
    global money

    if money <= 0:
        print("You have lost all of your money.")
        return False
    else:
        play_again = input("Do you want to play again? (y/n): ")

    if play_again == "y":
        return True
    else:
        print("You finished with $"+str(money)+". Come back soon!" )
        return False



def reset():
    global deck
    global is_player_turn
    global player_hand
    global dealer_hand
    global amount_bet
    global amount_bet_2
    global compare_count
    global has_split

    player_hand = []
    dealer_hand = []
    deck = []
    is_player_turn = True

    amount_bet = 0
    amount_bet_2 = 0

    compare_count = 0

    has_split = False


def bet():
    global money
    global amount_bet

    has_bet = False
    print("Current money:", money)

    while not has_bet:
        amount_bet = input("How much money would you like to bet?: ")
        try:
            amount_bet = int(amount_bet)
            if amount_bet > money:
                print("You don't have that much money! Please try again.")
                amount_bet = 0
                bet()
            elif amount_bet < 0:
                print("That is a negative number. Please try again with a positive number.")
            elif amount_bet == 0:
                print("You cannot bet 0 dollars. Please try again with a positive number.")
            else:
                print("Your bet has been accepted.")
                has_bet = True
        except:
            print("Please enter an integer.")


def pick_random_card(hand_to_deal):
    random_card = random.choice(deck)
    deck.remove(random_card)
    hand_to_deal.append(random_card)

def deal():
    global player_hand
    global dealer_hand

    #player_hand.append(deck.pop(6))
    #player_hand.append(deck.pop(18))

    player_hand.append(deck.pop())
    dealer_hand.append(deck.pop())
    player_hand.append(deck.pop())
    dealer_hand.append(deck.pop())


def get_hand_value(hand):
    total = 0
    aces = 0
    for card in hand:
        total += get_card_value(card)

        if card[:-1] == "A":
            aces += 1

    while aces > 0 and total > 22:
        total -= 10
        aces -= 1

    return total

def check_bust(hand):
    global money
    global amount_bet

    hand_total = get_hand_value(hand)

    if hand_total >= 22:
        return True
    else:
        return False


def player_action(hand, bet):
    global player_hand
    global player_hand_2
    global is_player_turn
    global amount_bet
    global amount_bet_2
    global dealing_playerhand_1

    print("\n")

    split()

    stand = False
    while not stand:
        print("Current hand:", *hand)
        print("Total Value:", get_hand_value(hand))
        print("Amount Bet:", bet)
        print("\nDealer hand:", *dealer_hand)

        if check_bust(hand):
            print("You bust :(. Moving on.")
            return

        action = input("Do you want to hit on your first hand? (y/n): ")
        if action.lower() == "y":
            pick_random_card(player_hand)
        else:
            print("Moving on.")


def compare(hand, bet):
    global dealer_hand
    global player_hand
    global player_hand_2
    global amount_bet
    global amount_bet_2
    global money

    total = get_hand_value(hand)
    dealer_total = get_hand_value(dealer_hand)

    print()
    print("Hand comparing:", *hand)
    print("Amount Bet:", bet)
    print("Total value:", total)
    print()
    print("Dealer hand:", *dealer_hand)
    print("Total value:", dealer_total)
    print()

    if total < 22:
        if dealer_total < 22:
            if total == 21 and len(hand) == 2 and len(player_hand_2) == 0 and dealer_total != 21:
                print("You have blackjack and the dealer doesn't!"
                      "\nYou get a bonus of 1.5x your original bet!")
                money += bet + bet/2
            elif total == dealer_total:
                print("You tied. Neither of you get any money.")
            elif total > dealer_total:
                print("You win!")
                money += bet
            elif total < dealer_total:
                print("So close, but you lost :(. You lose your money")
                money -= bet
        else:
            print("The dealer busted, so you win!")
            money += bet
    elif total > 22:
        print("You busted, so you lose money :(")
        money -= bet

    print("Current money:", money)

    return


def dealer_action(hand):
    total = get_hand_value(hand)

    while total < 17:
        total = get_hand_value(hand)

        print("Dealer hand:", *hand)
        print("Total value:", total)

        pick_random_card(hand)

        if total >= 22:
            print("Dealer busts!")




# main
while playing == True:
    reset()
    shuffle(suits, numbers)
    deal()
    bet()


    player_action(player_hand, amount_bet)

    if player_hand_2 != []:
        player_action(player_hand_2, amount_bet_2)

    dealer_action(dealer_hand)

    compare(player_hand, amount_bet)

    if player_hand_2 != []:
        compare(player_hand_2, amount_bet_2)

    if try_again() == True:
        playing = True

quit()