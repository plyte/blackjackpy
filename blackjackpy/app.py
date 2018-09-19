import numpy as np

class Player:

      def __init__(self, name, balance = 0):
            self.name = name
            self.balance = balance
            self.cards_in_hand = []

      def bet(self, how_much):
            self.balance -= how_much
      
      def hit(self, deck):
            if (len(deck) == 0):
                  raise ValueError
            else:
                  self.cards_in_hand.append(deck.pop(0))



def generate_deck(num_cards):

      deck = []

      if num_cards % 52 != 0 or num_cards == 0: 
            raise ValueError('The number of cards must be a multiple of 52')
      
      amount_of_each = num_cards/13

      for i in range(1, 14):
            if i < 11:
                  deck.append([str(i)]*amount_of_each)
            if i == 11:
                  deck.append(['J']*amount_of_each)
            if i == 12:
                  deck.append(['Q']*amount_of_each)
            if i == 13:
                  deck.append(['K']*amount_of_each)

      deck = np.asarray(deck)
      deck = list(deck.flatten())

      return deck
