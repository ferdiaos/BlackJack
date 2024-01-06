# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 14:55:37 2024

@author: ferdi
"""

import random

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        if self.rank == 1:
            return f"Ace of {self.suit}"
        elif self.rank <= 10:
            return f"{self.rank} of {self.suit}"
        else:  # Royal cards
            royal_names = {11: "Jack", 12: "Queen", 13: "King"}
            return f"{royal_names[self.rank]} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for rank in range(1, 14) for suit in ["d", "c", "h", "s"]]

    def pop_card(self):
        return self.cards.pop(random.randint(0, len(self.cards) - 1))

class HandOfCards:
    def __init__(self, num_cards):
        self.deck = Deck()
        self.hand = []
        for _ in range(num_cards):
            self.hand.append(self.deck.pop_card())

    def __str__(self):
        return "\n".join(str(card) for card in self.hand)

# Define a function to calculate the value of a hand, considering aces
def calculate_hand_value(hand):
   value = 0
   aces = 0
   for card in hand:
       rank = card.rank
       if rank == 1:  # Ace
           aces += 1
       elif 2 <= rank <= 10:
           value += rank
       else:  # Face cards
           value += 10

   # Adjust for aces
   while aces > 0 and value + 11 > 21:
       value += 1
       aces -= 1
   value += aces * 11
   return value

# Function to handle a player's turn
def player_turn(player_name, hand):
   print(f"{player_name}'s turn:")
   hand_value = calculate_hand_value(hand.hand)  # Calculate initial hand value
   print(hand)
   print(f"Hand value: {hand_value}")

   # Check for blackjack immediately
   if hand_value == 21:
       print("Blackjack!")
       return True  # Player has blackjack, no more turns

   while True:
       choice = input("Hit or pass? (h/p): ")
       if choice.lower() == "h":
           hand.hand.append(hand.deck.pop_card())
           print(hand)
           hand_value = calculate_hand_value(hand.hand)
           print(f"Hand value: {hand_value}")
           #check for blackjack on inital 2 cards
           if len(hand.hand)==2 and hand_value==21:
               print('Blackjack!')
               return True
           if hand_value > 21:
               print(f"{player_name} busts! Hand value: {hand_value}")
               return False  # Player busts
       elif choice.lower() == "p":
           return True  # Player passes
       else:
           print("Invalid choice. Please enter 'h' or 'p'.")

# Function to handle the dealer's turn
def dealer_turn(dealer_hand):
   print("\nDealer's turn:")
   while calculate_hand_value(dealer_hand.hand) < 17:
       dealer_hand.hand.append(dealer_hand.deck.pop_card())
   print(f'\n{dealer_hand}')  # Print dealer's final hand

# Main game logic
def play_blackjack():
   num_players = int(input("Enter the number of players: "))
   player_names = [input(f"Enter name for Player {i + 1}: ") for i in range(num_players)]

   # Create dealer hand
   dealer_hand = HandOfCards(2)

   # Create player hands
   player_hands = [HandOfCards(2) for _ in range(num_players)]

   # Iterate through player turns
   for i, (player_name, player_hand) in enumerate(zip(player_names, player_hands)):
       if not player_turn(player_name, player_hand):  # Player busted
           continue

   # Dealer's turn
   dealer_turn(dealer_hand)

   # Determine winners and losers
   dealer_value = calculate_hand_value(dealer_hand.hand)
   print(f"Dealer's final hand value: {dealer_value}")

   for i, (player_name, player_hand) in enumerate(zip(player_names, player_hands)):
       player_value = calculate_hand_value(player_hand.hand)
       print(f"{player_name}'s final hand value: {player_value}")
       if player_value > 21:
           print(f"{player_name} loses.")
       elif player_value > dealer_value or dealer_value > 21:
           print(f"{player_name} wins!")
       else:
           print(f"{player_name} ties with the dealer.")
           