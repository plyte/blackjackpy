import numpy as np

from random import shuffle

class Hand:

      def __init__(self):
            self.cards = []
            self.current_bet = 0
      
      def hit(self, deck):
            if (len(deck) == 0):
                  raise ValueError('Deck is empty')

            self.cards.append(deck.pop(0))

      def bet(self, how_much):
            self.current_bet = self.current_bet + how_much

      def surrender(self):
            self.cards = []
            self.current_bet = 0


class Player:

      def __init__(self, name, balance = 0):
            self.name = name
            self.balance = balance
            self.hands = [Hand()]
            self.stand_flag = False
            self.total_bet = 0

                  
      def bet(self, how_much, hand=0):
            if how_much > self.balance:
                  raise ValueError('You bet above your available balance: {}'.format(self.balance))

            self.total_bet += how_much
            self.hands[hand].bet(how_much)
            self.balance -= self.hands[hand].current_bet

      def hit(self, deck, hand=0):
            self.hands[hand].hit(deck)

      def surrender(self, hand=0):
            if len(self.hands[hand].cards) > 2:
                  raise RuntimeError('You must have 2 or less cards in hand to surrender')
            
            if self.hands[hand].current_bet == 0:
                  raise RuntimeError('You must have bet to surrender')

            self.balance += self.hands[hand].current_bet / 2

            if len(self.hands) > 1:
                  self.hands.pop(hand)
      
      def _split_hand(self, hand):
            
            current_hand = hand
            current_bet = current_hand.current_bet
            card_to_split_with = current_hand.cards.pop(0)
            
            new_hand = Hand()
            new_hand.cards.append(card_to_split_with)
            new_hand.current_bet = current_bet

            self.hands.append(new_hand)

      def stand(self):
            self.stand_flag = True

      def split(self, hand=0):
            """
            If the player contains two of the same denominations then the user
            may split his/her hand into two hands that are to be evaluated seperately 
            and then the best is doubled
            """
            current_hand = self.hands[hand]

            if (current_hand.current_bet*2 > self.balance):
                  raise ValueError('You do not have enough balance to complete this bet')

            if (len(current_hand.cards) != 2):
                  raise ValueError('There are not enough cards in the hand to split')
            
            if (current_hand.cards[0] == current_hand.cards[1]):
                  self._split_hand(current_hand)
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