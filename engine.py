# libraries
import random


# blackjack class
class Blackjack:
    def __init__(self):
        # variables and lists
        self.suits = ["♠", "♥", "♦", "♣"]
        self.numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.deck = []

        self.player_hand = []
        self.player_hand_2 = []
        self.dealer_hand = []

        self.money = 1000
        self.amount_bet = 0
        self.amount_bet_2 = 0

        self.dealing_playerhand_1 = True

        self.compare_count = 0

        self.has_split = False

    def pick_random_card(self, hand_to_deal):
        random_card = random.choice(self.deck)
        self.deck.remove(random_card)
        hand_to_deal.append(random_card)

    def reset(self):
        self.player_hand = []
        self.dealer_hand = []
        self.deck = []

        self.amount_bet = 0
        self.amount_bet_2 = 0

        self.compare_count = 0

        self.has_split = False

    def shuffle(self):
        for _ in range(0, 6):
            for n in self.numbers:
                for s in self.suits:
                    self.deck.append(n + s)

        random.shuffle(self.deck)

    def deal(self):
        self.player_hand.append(self.deck.pop())
        self.dealer_hand.append(self.deck.pop())
        self.player_hand.append(self.deck.pop())
        self.dealer_hand.append(self.deck.pop())

    def bet(self):
        has_bet = False
        print("Current money:", self.money)

        while not has_bet:
            self.amount_bet = input("How much money would you like to bet?: ")
            try:
                self.amount_bet = int(self.amount_bet)
                if self.amount_bet > self.money:
                    print("You don't have that much money! Please try again.")
                elif self.amount_bet < 0:
                    print("That is a negative number. Please try again with a positive number.")
                elif self.amount_bet == 0:
                    print("You cannot bet 0 dollars. Please try again with a positive number.")
                else:
                    print("Your bet has been accepted.")
                    has_bet = True
            except:
                print("Please enter an integer.")

    def split(self):
        if len(self.player_hand) == 2 and check_split(self.player_hand) and self.has_split == False:
            print("Your hand:", *self.player_hand)
            print("Total value:", get_hand_value(self.player_hand))
            print("\nDealer hand:", self.dealer_hand[0], "XX \n")
            action = input("Do you want to split (hit/stand later)? (y/n): ")

            if action.lower() == "y":
                self.player_hand_2.append(self.player_hand.pop(1))
                self.amount_bet_2 = self.amount_bet

                print("Hand 1:", *self.player_hand)
                print("Amount Bet:", self.amount_bet)
                print("Hand 2:", *self.player_hand_2)
                print("Amount Bet:", self.amount_bet_2)
                print()
                print("Dealing extra card to each hand")
                self.pick_random_card(self.player_hand)
                self.pick_random_card(self.player_hand_2)

                print("Hand 1:", *self.player_hand)
                print("Hand 2:", *self.player_hand_2)
                print("\n")

                self.has_split = True

    def player_action(self, hand, bet):
        print("\n")

        if has_blackjack(hand):
            print("You have blackjack! As long as the dealer doesn't, you will win with a bonus!")
            print("Let's see what the dealer has...")
            quit()

        stand = False
        while not stand:
            print("Current hand:", *hand)
            print("Total Value:", get_hand_value(hand))
            print("Amount Bet:", bet)
            print("\nDealer hand:", *self.dealer_hand[0], "XX")

            if check_bust(hand):
                print("You bust :(. Moving on.")
                return

            action = input("Do you want to hit? (y/n): ")
            if action.lower() == "y":
                self.pick_random_card(hand)
            else:
                print("Moving on.")
                stand = True

    def dealer_action(self, hand):
        total = get_hand_value(hand)

        if has_blackjack(hand):
            print("Dealer hand:", *hand)
            print("Dealer has blackjack!")
            return

        while total < 17:
            total = get_hand_value(hand)

            print("Dealer hand:", *hand)
            print("Total value:", total)

            self.pick_random_card(hand)

            total = get_hand_value(hand)

            if total >= 22:
                print("Dealer busts!")
                print("Dealer hand:", *hand)
                print("Total value:", total)

    def compare(self, hand, bet):
        total = get_hand_value(hand)
        dealer_total = get_hand_value(self.dealer_hand)

        print()
        print("Hand comparing:", *hand)
        print("Amount Bet:", bet)
        print("Total value:", total)
        print()
        print("Dealer hand:", *self.dealer_hand)
        print("Total value:", dealer_total)
        print()

        if total < 22:
            if dealer_total < 22:
                if total == 21 and len(hand) == 2 and dealer_total != 21:
                    print("You have blackjack and the dealer doesn't!"
                          "\nYou get a bonus of 1.5x your original bet!")
                    self.money += bet + bet / 2
                elif total == dealer_total:
                    print("You tied. Neither of you get any money.")
                elif total > dealer_total:
                    print("You win!")
                    self.money += bet
                elif total < dealer_total:
                    print("So close, but you lost :(. You lose your money")
                    self.money -= bet
            else:
                print("The dealer busted, so you win!")
                self.money += bet
        elif total > 22:
            print("You busted, so you lose money :(")
            self.money -= bet

        print("Current money:", self.money)

        return

    def try_again(self, money):
        if money <= 0:
            print("You have lost all of your money.")
            return False
        else:
            play_again = input("Do you want to play again? (y/n): ")

        if play_again == "y":
            return True
        else:
            print("You finished with $" + str(money) + ". Come back soon!")
            return False

game = Blackjack()


# helper functions
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


def get_hand_value(hand):
    total = 0
    aces = 0
    for card in hand:
        total += get_card_value(card)

        if card[:-1] == "A":
            aces += 1

    while aces > 0 and total >= 22:
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

def has_blackjack(hand):
    if get_hand_value(hand) == 21 and len(hand) == 2:
        return True
    else:
        return False