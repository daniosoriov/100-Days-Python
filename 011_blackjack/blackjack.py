
import random, blackjack_art as ba
from os import system

# Create the cards with 6 decks.
set_cards = ['A', 'J', 'Q', 'K'] + list(range(2, 11))
cards = set_cards * 24

def deal_card(hand):
    '''Deals a card and sets it in hand. It returns the total value of the cards in hand.'''
    global cards
    card = random.choice(cards)
    hand.append(card)
    cards.remove(card)
    return hand_score(hand)

def hand_score(hand):
    '''Calculates the total value of hand and returns it as an int.'''
    sum = 0
    for n in hand:
        if n in ['J', 'Q', 'K']:
            sum += 10
        elif n == 'A':
            if sum < 11:
                sum += 11
            else:
                sum += 1
        else:
            sum += n
    return sum

def show_hand(hand, human = True, final = False):
    '''Prints the hand showing the cards for the player (human=True) or the dealer (human=False) and the score (final=True).'''
    text = 'final' if final else 'current'
    if human:
        print(f'    Your cards: {hand}, {text} score: {hand_score(hand)}')
    else:
        show = hand if final else f'[{hand[0]}]'
        text = f'    Dealer cards: {show}'
        if final:
            text += f', final score: {hand_score(hand)}'
        print(text)

finish = False
win_human, win_comp, draws = 0, 0, 0

print(ba.BLACKJACK_LOGO)
print('Welcome to blackjack!')
while not finish:
    hand_human, hand_comp = [], []
    # First, deliver a card to player, one to dealer, one to player and another one to dealer
    deal_card(hand_human)
    deal_card(hand_comp)
    # Calculate the score both players have
    score_human = deal_card(hand_human)
    score_comp = deal_card(hand_comp)

    # Showing hands, only one for the dealer
    show_hand(hand_human)
    show_hand(hand_comp, human=False)

    stop_game = False
    while not stop_game:
        more = input('Get another card (h) or stand (s)?: ')
        while more not in ['h', 's']:
            more = input('Only type h or s: ')
        
        # Hit the player with another card
        if more == 'h':
            score_human = deal_card(hand_human)
            show_hand(hand_human)
            show_hand(hand_comp, human=False)
            # If the player exceeds 21, the game is over
            if score_human > 21:
                stop_game = True
                print('You lost!')
                win_comp += 1

        # Stand and let the dealer play, then show the results
        elif more == 's':
            stop_game = True
            while score_comp < 17:
                score_comp = deal_card(hand_comp)
            show_hand(hand_human, final=True)
            show_hand(hand_comp, human=False, final=True)
            
            # The different outcomes
            if score_comp > 21:
                print('You win')
                win_human += 1
            elif score_human == score_comp:
                print('Draw')
                draws += 1
            elif score_comp > score_human:
                print('You lost')
                win_comp += 1
            elif score_comp < score_human:
                print('You win')
                win_human += 1
            else:
                print('I missed this case, please report', score_human, score_comp)

        # The game stopped, show accumulated results
        if stop_game:
            print(f'Score is you: {win_human}, dealer: {win_comp}, and draws: {draws}')
            print()
            # Play again?
            one_more = input('Play again? y or n: ')
            while one_more not in ['y', 'n']:
                one_more = input('Play again? Only type y or n: ')
            if one_more == 'y':
                system('clear')
            else:
                print('Thank you, and goodbye!')
                finish = True
