# Blackjack
# 9/3/26
__author__ = "Deven Surana"


from engine import Blackjack

game = Blackjack()

# main

while True:
    game.reset()
    game.shuffle()
    game.deal()
    game.bet()

    game.split()

    game.player_action(game.player_hand, game.amount_bet)

    if game.player_hand_2 != []:
        game.player_action(game.player_hand_2, game.amount_bet_2)

    game.dealer_action(game.dealer_hand)

    game.compare(game.player_hand, game.amount_bet)

    if game.player_hand_2 != []:
        game.compare(game.player_hand_2, game.amount_bet_2)

    if not game.try_again(game.money):
        break

quit()