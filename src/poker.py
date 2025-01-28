import random
from cards import Deck
from player import Player, Player_actions
import numpy as np


def determine_winner(player_hands, community_cards):
    return random.choice(range(len(player_hands)))

def play_game(players, n_round, display=False):
    out_players = []

    # Rising only by constant amount
    basic_bet = 50
    current_bet = basic_bet
    current_pool = 0 

    deck = Deck()

    for player in players:
        player.add_cards(deck.deal_cards())
    
    community_cards = []
    betting_rounds = ["Pre-Flop", "Flop", "Turn", "River"]


    for idx_round, round_name in enumerate(betting_rounds):
        if display:
            print(f"\n--- {round_name} ---")
        
        # Firs(deal 3 cards), other(deal 1 card)
        if round_name == "Flop":
            community_cards.extend(deck.first_draw()) 
        elif round_name in ["Turn", "River"]:
            community_cards.extend(deck.next_draw()) 

        # Display each player's hand
        if display:
            for player in players:
                player.display_hand(community_cards)

        while True:
            all_matched = True
            for player in players:
                player.calculate_score(community_cards)
                action = player.make_decision(current_bet, basic_bet, n_round) 
                
                if action == Player_actions.FOLD.value:
                    if display:
                        print(f"{player.name} has folded!")
                    out_players.append(player)
                    players.remove(player)
                elif action == Player_actions.RISE.value:
                    current_bet += basic_bet
                    current_pool += player.add_bet(current_bet)
                    if display:
                        print(f"{player.name} raises the bet to {current_bet}.")
                    all_matched = False
                elif action == Player_actions.CHECK.value:
                    change = player.add_bet(current_bet) 
                    if change == -1:
                        if display:
                            print(f"{player.name} has folded!")
                        out_players.append(player)
                        players.remove(player) 
                    else:
                        current_pool += change
                        if display:
                            print(f"{player.name} calls the current bet of {current_bet}.")
                else:
                    if display:
                        print(f"{player.name} made an invalid move.")

            # If only one player remains, they win the pot
            if len(players) == 1:
                if display:
                    print(f"{players[0].name} wins by default!")
                break
            
            # Exit the betting round if all active players have matched the current bet
            if all_matched:
                break

        if display:
            print(f"current pool: {current_pool}")


        # Check if the game ends early
        if len(players) == 1:
            if display:
                print(f"{players[0].name} wins by default!")
            break

    players_scores = np.array([ player.get_score() for player in players ])
    best_score = np.max(players_scores)

    for idx, player in enumerate(players):
        if players_scores[idx] < best_score:
            out_players.append(player)
            players.remove(player)

    # At Draw highest card wins
    if len(players)>1:
        players_high_cards = np.array([ player.get_high_card() for player in players ])
        best_score = np.max(players_high_cards)
        for idx, player in enumerate(players):
            if players_high_cards[idx] < best_score:
                out_players.append(player)
                players.remove(player)

    prize = current_pool/len(players)

    for player in players:
        player.add_win(prize)
        out_players.append(player)
        if display:
            print(f'Winner: {player.name}')
            print(player.balance)


    return out_players

'''
# For testing
def main():

    amount_of_players = 2
    amount_of_rounds = 10
    starting_balance = 2000
    
    players = [Player(f'Player {i + 1}', amount_of_players, starting_balance) for i in range(amount_of_players)]

    for n_round in range(amount_of_rounds):
        players = play_game(players, n_round, True)


if __name__ == "__main__":
    main()
'''