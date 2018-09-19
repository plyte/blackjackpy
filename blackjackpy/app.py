import numpy as np

from random import shuffle

class Player:

      def __init__(self, name, balance = 0):
            self.name = name
            self.balance = balance
            self.cards_in_hand = []
            self.stand_flag = False

      def bet(self, how_much):
            self.balance -= how_much

      def _place_in_hand(self, card, hand=0):
            print('Placed card in hand')
            if len(self.cards_in_hand) != 0 and isinstance(self.cards_in_hand[0], list):
                  self.cards_in_hand[hand].append(card)
            else:
                  self.cards_in_hand.append(card)

      
      def _draw(self, deck, hand=0):
            print('Drawing card')
            if (len(deck) == 0):
                  raise ValueError
            else:
                  self._place_in_hand(deck.pop(0))

      def hit(self, deck, hand=0):
            print('Player hit')
            self._draw(deck, hand)

      def stand(self):
            self.stand_flag = True

      def split(self):
            """
            If the player contains two of the same denominations then the user
            may split his/her hand into two hands that are to be evaluated seperately 
            and then the best is doubled
            """
            if (len(self.cards_in_hand) == 0):
                  raise ValueError('There are not enough cards in the hand to split')
            
            if (self.cards_in_hand[0] == self.cards_in_hand[1]):
                  self.cards_in_hand = [[val] for val in self.cards_in_hand]
            else:
                  raise ValueError('The cards are not of the same denomination')


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

def shuffle_deck(deck):
      shuffle(deck)
      return deck