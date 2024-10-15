from datetime import datetime as dt
from time import sleep
import random

BALANCE = 2000


def output(string):
    print(f"{dt.now().strftime('%Y-%m-%d %H:%M:%S')} {string}")


def shuffle(d):
    random.shuffle(d)
    return d


def cut(d):
    cut_idx = random.randint(0, 51)
    return d[cut_idx:] + d[:cut_idx]


def calculateHand(hand):
    hand_value = 0
    for c in hand:
        card_value = c[:-1]

        if card_value == "A":
            card_value = 11
        elif card_value in ["J", "Q", "K"]:
            card_value = 10
        else:
            card_value = int(card_value)

        hand_value += card_value

    if hand_value > 21:
        for c in hand:
            if c[:-1] == "A":
                hand_value -= 10
                if hand_value <= 21:
                    break

    return hand_value


def printHand(hand, player_name):
    hand_value = calculateHand(hand)
    out_str = f"{player_name} ({hand_value}):"
    for y in hand:
        out_str += f" {y}"
    output(out_str)


def printHands(hands_):
    output("--------------------------------")
    for x in range(len(hands_)):
        if len(hands_[x]) < 2:
            output(f"[ERROR] invalid hand: {hands_[x]}")
        elif x == len(hands_) - 1:
            output(f"DEALER (?): {hands_[x][0]} ??")
        else:
            printHand(hands_[x], f"PLAYER {x + 1}")
    output("--------------------------------")


if __name__ == '__main__':
    output(f"Welcome to Blackjack. You start with ${BALANCE}.")
    random.seed(dt.now().timestamp())

    DECK = []
    for i in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']:
        for j in ['S', 'D', 'C', 'H']:
            DECK.append(i + j)
    DECK *= 4
    output("Shuffling deck...")
    deck_ = cut(shuffle(shuffle(DECK)))

    r = 0
    num_players = 1
    wager = input(f"Enter your wager (q to quit) [Balance: ${BALANCE}]: ")
    while wager.lower() not in ["q", "quit"]:
        try:
            BALANCE -= int(wager)
        except ValueError:
            output("[ERROR] invalid wager. Please enter an integer.")
            wager = input("Enter your wager (q to quit): ")
            continue

        r += 1
        hands = [[] for i in range(num_players + 1)]
        for _ in range(2):
            for h in hands:
                h.append(deck_[0])
                deck_ = deck_[1:]

        for i in range(len(hands) - 1):
            player_name = f"PLAYER {i + 1}"
            while True:
                printHands(hands)
                if calculateHand(hands[i]) == 21 and len(hands[i]) == 2:
                    output(f"{player_name}: BLACKJACK!")
                    break
                move = input(f"{player_name} Hit (h) or stand (s): ")
                while move.lower() not in ["h", "hit", "s", "stand"]:
                    move = input("[ERROR] invalid input. Hit (h) or stand (s): ")

                if move.lower() in ["h", "hit"]:
                    hands[i].append(deck_[0])
                    deck_ = deck_[1:]
                    # printHand(hands[i], player_name)
                elif move.lower() in ["s", "stand"]:
                    break

                if calculateHand(hands[i]) > 21:
                    output(f"PLAYER {i + 1} busts!")
                    break

        printHands(hands)
        output("DEALER's turn...")
        printHand(hands[-1], "DEALER")
        dealer_score = calculateHand(hands[-1])
        while dealer_score < 17:
            sleep(2)
            output("DEALER hits.")
            sleep(1)
            hands[-1].append(deck_[0])
            deck_ = deck_[1:]
            printHand(hands[-1], "DEALER")
            dealer_score = calculateHand(hands[-1])

        if calculateHand(hands[-1]) > 21:
            output("DEALER busts!")
        else:
            output("DEALER stands.")

        for i in range(len(hands) - 1):
            out_ln = f"PLAYER {i + 1}: "
            player_score = calculateHand(hands[i])
            if player_score == 21 and dealer_score != 21 and len(hands[i]) == 2:
                out_ln += "WIN"
                BALANCE += 2.5 * int(wager)
            elif (dealer_score < player_score <= 21) or (player_score <= 21 < dealer_score):
                out_ln += "WIN"
                BALANCE += 2 * int(wager)
            elif (player_score < dealer_score <= 21) or player_score > 21:
                out_ln += "LOSE"
            else:
                out_ln = "PUSH"
                BALANCE += int(wager)

            output(out_ln)

        if len(DECK) <= 104:
            output("Shuffling deck...")
            deck_ = cut(shuffle(shuffle(DECK)))

        wager = input(f"Enter your wager (q to quit) [Balance: ${BALANCE}]: ")
