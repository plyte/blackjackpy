import numpy as np

from random import shuffle

class Blackjack:

      def __init__(self, minimum_bet):
            self.minimum_bet = minimum_bet
            self.actions = ['hit', 'bet', 'double down', 'split', 'stand']
            self.start_flag = False
            self.dealer = Dealer('Dealer')
            self.players = []
            self.deck = []

      def start(self):
            self.start_flag = True

      def welcome_message(self):
            print('Welcome to blackjackpy built by Matthew Jones')

            deck = generate_deck(num_cards=52)
            self.deck = shuffle_deck(deck)

            num_players = int(raw_input('Please indicate the number of players: '))
            starting_balance = int(raw_input('Please indicate the starting balance: '))

            for i in range(int(num_players)):

                  name = raw_input('Please input player {}\'s name: '.format(i))
                  self.players.append(Player(name, balance=starting_balance))

            self.start()
            

      def show_cards(self):
            print('')
            print('Dealers face up card: {}'.format(self.dealer.hands[0].cards[0]))
            print('')

            for player in self.players:
                  
                  print('{}\'s hand(s):'.format(player.name))
                  for hand in player.hands:
                        print(hand.cards)

      def display_finish_message(self):

            print('There are no more cards in the deck!')
            print('The game is now over')

      def round(self):

            if (len(self.deck)):
                  self.display_finish_message()
            else:
                  self.dealer.deal(self.players, self.deck)

                  print('')
                  print('================================Round Starts================================')
                  print('')

                  print('')
                  print('Initial bets are placed (minimum of {})'.format(self.minimum_bet))
                  print('')

                  for player in self.players:
                        player.bet(self.minimum_bet)

                  self.display_balances()
                  self.show_cards()

                  stopping_condition_has_been_hit = False
                  while (not stopping_condition_has_been_hit):

                        for player in self.players:
                              print('{}\'s turn'.format(player.name))
                              self.display_options()
                              action = raw_input('Please choose an action: ')

      def evaluate_action(self, player, action):

            switcher = {
                  1: "bet",
                  2: "split",
                  3: "hit",
                  4: "stand",
                  5: "double down",
            }

            def bet(player, hand=0):
                  how_much = raw_input('How much would you like to bet?: ')
                  player.bet(how_much)
            
            def split(player):
                  player.split()
            
            def hit(player):
                  player.hit(self.deck)

            def double_down(player):
                  player.double_down(self.deck)

            def stand(player):
                  player.stand()
                  print('Round has ended for {}'.format(player.name))
                  print('Once the dealer\'s turn is over the hand will be evaluated')

            if action in self.actions:
                  switch (action):




      def display_options(self):

            to_print = [action + ', ' for action in self.actions]
            print_out = ''.join(to_print)
            print('Actions you can choose: {}'.format(print_out))


      def display_balances(self):

            for player in self.players:
                  print('{}\'s current balance: {}'.format(player.name, player.balance))



      

class Hand:

      def __init__(self):
            self.cards = []
            self.current_bet = 0
            self.stand_flag = False
            self.evaluate_map = self._generate_evaluate_map()
            self.total_value = 0

      def _generate_evaluate_map(self):
            evaluate_map = {}

            evaluate_map['A'] = [1, 11]
            for i in range(2, 11):
                  evaluate_map[str(i)] = i
            evaluate_map['K'] = 10
            evaluate_map['Q'] = 10
            evaluate_map['J'] = 10

            return evaluate_map
      
      def hit(self, deck):
            if (len(deck) == 0):
                  raise ValueError('Deck is empty')

            self.cards.append(deck.pop(0))

      def bet(self, how_much):
            self.current_bet = self.current_bet + how_much

      def surrender(self):
            self.cards = []
            self.current_bet = 0

      def _calculate(self):

            total = 0

            for card in self.cards:
                  if isinstance(self.evaluate_map[card], list):
                        total += max(self.evaluate_map[card])
                  else:
                        total += self.evaluate_map[card]

            if total > 21:
                  total = 0
                  for card in self.cards:
                        if isinstance(self.evaluate_map[card], list):
                              total += max(self.evaluate_map[card])
                        else:
                              total += self.evaluate_map[card]

            return total

      def evaluate(self):

            total = self._calculate()      
            self.total_value = total    

            return total




class Player:
      """
      Class to define the player and their actions
      actions: hit, bet, stand, split, surrender, and insure. 
      The player may be instantiated by including a name and a balance.
      If a balance is not specified a default of 0 is applied.
      """

      def __init__(self, name, balance = 0):
            self.name = name
            self.balance = balance
            self.hands = [Hand()]
            self.stand_flag = False
            self.total_bet = 0

                  
      def bet(self, how_much, hand=0):
            """
            The bet action is utilized to update the current bet of the specific hand.
            Once called the user increases the bet of the specific hand passed through the hand 
            argument

            Args:
                  how_much (int): The amonut to bet
                  hand (int): The specific hand contained in the hands array (i.e. hand=0 for first)

            Returns:
                  void
            """
            if how_much > self.balance:
                  raise ValueError('You bet above your available balance: {}'.format(self.balance))

            self.total_bet += how_much
            self.hands[hand].bet(how_much)
            self.balance -= self.hands[hand].current_bet

      def hit(self, deck, hand=0):
            """
            The player is given another card for the specific hand specified by the hand argument

            Args:
                  deck (list(str)): The array containing the cards to distribute
                  hand (int): The specific hand contained in the hands array (i.e. hand=0 for first)
            
            Returns:
                  void

            Examples:
                  >>> player.hit(hand=1)
            """
            self.hands[hand].hit(deck)

      def surrender(self, hand=0):
            """
            The player may surrender the hand specified by the hand argument. This causes 
            the hand to be over and half the current bet of the hand to be reimbursed to the player

            Args:
                  hand (int): The specific hand contained in the hands array (i.e. hand=0 for first)

            Returns:
                  void
            
            Examples:
                  >>> player.surrender(hand=1)
            """
            if len(self.hands[hand].cards) > 2:
                  raise RuntimeError('You must have 2 or less cards in hand to surrender')
            
            if self.hands[hand].current_bet == 0:
                  raise RuntimeError('You must have bet to surrender')

            self.balance += self.hands[hand].current_bet / 2

            if len(self.hands) > 1:
                  self.hands.pop(hand)
      
      def _split_hand(self, hand):
            """
            Internal helper function that provides the logic for splitting
            """
            
            current_hand = hand
            current_bet = current_hand.current_bet
            card_to_split_with = current_hand.cards.pop(0)
            
            new_hand = Hand()
            new_hand.cards.append(card_to_split_with)
            new_hand.current_bet = current_bet

            self.hands.append(new_hand)

      def stand(self, hand=0):
            """
            The player may stand on the specific hand. If a player stands then the player 
            may no longer bet or hit for that specific hand. The hand is the evaluated against the
            dealer's hand

            Args:
                  hand (int): The specific hand contained in the hands array (i.e. hand=0 for first)

            Returns:
                  void
            """
            self.hands[hand].stand_flag = True

      def split(self, hand=0):
            """
            If the player contains two of the same denominations then the user
            may split his/her hand into two hands that are to be evaluated seperately 
            and then the bet is doubled.

            Args:
                  hand (int): The specific hand contained in the hands array (i.e. hand=0 for first)

            Returns:
                  void
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

      def double_down(self, deck, hand=0):
            """
            The player may double down. The player gets exactly one more card, the players bet
            doubles, and the turn ends.

            Args:
                  deck (list(str)): The array containing the cards to distribute
                  hand (int): The specific hand contained in the hands array (i.e. hand=0 for first)

            Returns:
                  void
            """

            current_hand = self.hands[hand]
            if (current_hand.current_bet == 0):
                  raise RuntimeError('You must have bet something before you double down')

            current_hand.hit(deck)
            current_hand.bet(current_hand.current_bet)
            self.stand_flag = True

class Dealer(Player):

      def hit(self, deck, hand=0):
            """
            The player is given another card for the specific hand specified by the hand argument

            Args:
                  deck (list(str)): The array containing the cards to distribute
                  hand (int): The specific hand contained in the hands array (i.e. hand=0 for first)
            
            Returns:
                  void

            Examples:
                  >>> dealer.hit(deck, hand=1)
            """
            total = self.hands[hand].evaluate()

            if total > 17:
                  raise RuntimeError('The dealer doesn\'t hit on a score of above 17')
            else:
                  self.hands[hand].hit(deck)
      
      def deal(self, players, deck, hand=0):

            for _ in range(2):

                  for player in players:
                        player.hands[hand].cards.append(deck.pop(0))

                  self.hands[hand].cards.append(deck.pop(0))
            

      def play(self, deck, hand=0):
            """
            The dealer 'plays' til a it either goes over or it hits a value greater than or equal to 17
            """

            stopping_condition_has_been_hit = False
            while (not stopping_condition_has_been_hit):

                  if self.hands[hand].evaluate() >= 17:
                        stopping_condition_has_been_hit = True
                  else:
                        self.hit(deck, hand)
      
      

def generate_deck(num_cards):

      deck = []

      if num_cards % 52 != 0 or num_cards == 0: 
            raise ValueError('The number of cards must be a multiple of 52')
      
      amount_of_each = num_cards/13

      for i in range(1, 14):
            if i == 1:
                  deck.append(['A']*amount_of_each)
            if i < 11 and i > 1:
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