# Blackjack
# 9/3/26
__author__ = "Deven Surana"


# libraries
import math
import random
import time


# variables and lists
# variables and lists
suits = ["♠", "♥", "♦", "♣"]
numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

deck = []

player_hand = []
player_hand_2 = []
dealer_hand = []

random_card = ""

money = 1000
amount_bet = 0
amount_bet_2 = 0
blackjack_bonus = 0

is_player_turn = True

dealing_playerhand_1 = True

compare_count = 0

# functions
def shuffle(suit, number):
    for i in range(0, 6):
        for number in numbers:
            for suit in suits:
                deck.append(number+suit)

    random.shuffle(deck)
    print(deck)

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

def play_game():
    global player_hand
    global dealer_hand
    global amount_bet
    global blackjack_bonus

    reset()
    shuffle(suits, numbers)
    deal()
    bet()

    if get_hand_value(player_hand) == 21:
        blackjack_bonus = amount_bet / 2
        blackjack_bonus += math.floor(blackjack_bonus)

    player_action()


def try_again():
    global money

    if money <= 0:
        return
    else:
        play_again = input("Do you want to play again? (y/n): ")

    if play_again == "y":
        play_game()
    else:
        print("You finished with $"+str(money)+". Come back soon!" )
        quit()



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
    tmp = 0
    for i in hand:
        tmp += get_card_value(i)

    if tmp > 22 and any("A" in item for item in hand):
        tmp -= 10

    return tmp

def check_bust(hand):
    global money
    global amount_bet

    hand_total = get_hand_value(hand)

    if hand_total >= 22:
        if any("A" in item for item in hand) and hand_total-10 < 22:
            return 0

        print("You bust! You lose :(.")
        print("(Hand:"," ".join(hand)+")")
        money -= amount_bet
        print("Current money:", money)

        return -1

has_split = False

def player_action():
    global player_hand
    global player_hand_2
    global is_player_turn
    global amount_bet
    global amount_bet_2
    global dealing_playerhand_1
    global has_split


    print("\n")


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
            print("\n")

            has_split = True

    #run if we have split
    if player_hand_2 != []:

        #PLAYER HAND 1
        if dealing_playerhand_1:
            if get_hand_value(player_hand) < 22:
                print("PLAYER HAND 1")
                print("Hand 1:", *player_hand)
                print("Total value:", get_hand_value(player_hand))
                print("Amount Bet:", amount_bet)
                print("\nDealer hand:", dealer_hand[0], "XX \n")

                action = input("Do you want to hit on your first hand? (y/n): ")
                if action.lower() == "y":
                    pick_random_card(player_hand)
                    player_action()
                else:
                    dealing_playerhand_1 = False
                    print("Moving on to your second hand.")
                    player_action()
            else:
                print("PLAYER HAND 1")
                print("Hand 1:", *player_hand)
                print("Total value:", get_hand_value(player_hand))
                print("You have busted on your first hand. Moving on to the second hand.")
                dealing_playerhand_1 = False
                player_action()

        #PLAYER HAND 2
        elif not dealing_playerhand_1:
            if get_hand_value(player_hand_2) <22:
                print("PLAYER HAND 2")
                print("Hand 2:", *player_hand_2)
                print("Total value:", get_hand_value(player_hand_2))
                print("Amount Bet:", amount_bet_2)
                print("\n Dealer hand:", dealer_hand[0], "XX \n")

                action = input("Do you want to hit on your second hand? (y/n): ")
                if action.lower() == "y":
                    pick_random_card(player_hand_2)
                    player_action()
                else:
                    dealer_action()
                    is_player_turn = False
                    return
            else:
                print("PLAYER HAND 2")
                print("Hand 2:", *player_hand_2)
                print("Total value:", get_hand_value(player_hand_2))
                print("You have busted on your second hand. Moving on to the dealers turn.")
                is_player_turn = False
                dealer_action()

    #run if we have not split
    else:
        if check_bust(player_hand) == -1:
            print()
            try_again()
            return

        print("Your hand:", *player_hand)
        print("Total value:", get_hand_value(player_hand))
        print("\nDealer hand:", dealer_hand[0], "XX \n")

        action = input("Do you want to hit? (y/n): ")
        if action.lower() == "y":
            pick_random_card(player_hand)
            player_action()
        else:
            print("\n Ok. It is now the dealers turn.")
            dealer_action()

            is_player_turn = False

def compare(hand, bet):
    global dealer_hand
    global player_hand
    global player_hand_2
    global amount_bet
    global amount_bet_2
    global money
    global compare_count

    compare_count += 1

    total = get_hand_value(hand)
    dealer_total = get_hand_value(dealer_hand)

    print()
    print("Hand comparing:", *hand)
    print("Amount Bet:", bet)
    print()
    print("Dealer hand:", *dealer_hand)
    print()

    if total < 22:
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
    elif total > 22:
        print("You busted, so you lose money :(")
        money -= bet

    if player_hand_2 != [] and compare_count == 1:
        print("Current money:", money)
        compare(player_hand_2, amount_bet_2)
        return


    print("Current money:", money)

    try_again()
    return


def dealer_action():
    global dealer_hand

    print("Dealer hand:", *dealer_hand)
    print("Total value:", get_hand_value(dealer_hand))

    hand_total = get_hand_value(dealer_hand)

    if hand_total < 17:
        pick_random_card(dealer_hand)
        dealer_action()
        return
    elif hand_total >= 22:
        print("Dealer busts!")

    compare(player_hand, amount_bet)



# main
play_game()
