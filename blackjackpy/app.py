import numpy as np

from random import shuffle
import os
import sys

_PAYOUT = 1.5

class Blackjack:

      def __init__(self, minimum_bet):
            self.minimum_bet = minimum_bet
            self.actions = 'bet (1), split (2), hit (3), stand (4), double down (5), and quit (6)'
            self.start_flag = False
            self.stop_flag = False
            self.dealer = Dealer('Dealer')
            self.players = []
            self.deck = []
            self.payout = _PAYOUT

      def start(self):

            self.start_flag = True

      def welcome_message(self):

            print('Welcome to blackjackpy built by Matthew Jones')
            print('Payout is {}'.format(_PAYOUT))

            deck = generate_deck(num_decks=2)
            self.deck = shuffle_deck(deck)

            num_players = int(input('Please indicate the number of players: '))
            starting_balance = int(input('Please indicate the starting balance: '))

            for i in range(int(num_players)):

                  name = input('Please input player {}\'s name: '.format(i))
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
            self.stop_flag = True

      def players_round(self):
            stopping_condition_has_been_hit = False
            while (not stopping_condition_has_been_hit):

                  for player in self.players:

                        for i, hand in enumerate(player.hands):
                              while (not hand.stand_flag):
                                    print('{}\'s turn'.format(player.name))
                                    self.display_options()

                                    action = int(input('Please choose an action: '))
                                    self.evaluate_action(player, action, i)

                  stopping_condition_has_been_hit = True

      def payout_round(self):
            dealers_hand = self.dealer.hands[0]
            dealers_hand_val = dealers_hand.evaluate()

            for player in self.players:

                  for hand in player.hands:
                        
                        if (hand.evaluate() > 21):

                              print('{} lost by bust with hand {}'.format(player.name, hand.cards))

                        elif ((dealers_hand_val > hand.evaluate()) and \
                              (dealers_hand_val <= 21) or \
                              (dealers_hand_val == hand.evaluate())):

                              print('{} lost with {} against the dealer\'s hand {}'\
                                    .format(player.name, hand.cards, dealers_hand.cards))
                        
                        else:

                              print('{}\'s score: {}'.format(player.name, hand.evaluate()))
                              print('{}\'s score: {}'.format('Dealer', dealers_hand.evaluate()))
                              print('{} won with {} against the dealer\'s hand {}'\
                                    .format(player.name, hand.cards, dealers_hand.cards))
                              player.balance += hand.current_bet * self.payout

                        self.clean_hand(hand)

            self.clean_hand(dealers_hand)

      def clean_hand(self, hand):

            hand.current_bet = 0
            hand.cards = []
            hand.total_value = 0
            hand.stand_flag = False

      def dealers_round(self):

            self.dealer.play(self.deck)

      def check_end_of_game(self):

            for player in self.players:

                  if player.balance <= 0:

                        player.end_game = False

            for player in self.players:

                  if player.end_game == True:
                        continue
                  else:
                        return False

            return True

      def check_blackjack(self):

            for player in self.players:
                  if player.hands[0].evaluate() == 21:
                        print('{} wins with a blackjack!'.format(player.name))
                        player.turn_end = True
            
            for player in self.players:
                  if player.turn_end:
                        continue
                  else:
                        return False

            return True

      def round(self):

            if (len(self.deck) == 0):
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

                  if self.check_blackjack():
                        self.turn_end = True

                  self.display_balances()
                  self.show_cards()

                  self.players_round()
                  if self.check_blackjack():
                        self.turn_end = True

                  self.dealers_round()

                  self.payout_round()
                  if self.check_end_of_game():
                        self.end_game = True

      def display_players_hand(self, player, hand):

            print('Your current hand: {}'.format(player.hands[hand].cards))


      def evaluate_action(self, player, action, hand):

            hand = hand

            def bet(player, hand):
                  how_much = int(input('How much would you like to add to your bet?: '))
                  player.bet(how_much, hand)
            
            def split(player, hand):
                  player.split()
            
            def hit(player, hand):
                  player.hit(self.deck, hand)
                  self.display_players_hand(player, hand)

            def stand(player, hand):
                  player.stand(hand)
                  print('')
                  print('Round has ended for {}'.format(player.name))
                  print('Once the dealer\'s turn is over the hand will be evaluated')
                  print('')

            def double_down(player, hand):
                  player.double_down(self.deck)

            def quit_game(player, hand):
                  print('Thanks for playing!')
                  sys.exit()

            switcher = {
                  1: bet,
                  2: split,
                  3: hit,
                  4: stand,
                  5: double_down,
                  6: quit_game
            }

            if action in range(7):
                  switcher.get(action)(player, hand)
            
      def display_options(self):

            print('Actions you can choose: {}'.format(self.actions))


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
            self.evaluate()

      def bet(self, how_much):
            self.current_bet = self.current_bet + how_much

      def surrender(self):
            self.cards = []
            self.current_bet = 0

      def _calculate(self):

            total = 0
            temp_total = 0

            for card in self.cards:
                  if isinstance(self.evaluate_map[card], list):
                        temp_total += max(self.evaluate_map[card])
                        if (temp_total > 21):
                              total += min(self.evaluate_map[card])
                        else:
                              total += max(self.evaluate_map[card])
                  else:
                        total += self.evaluate_map[card]

            if total > 21:
                  total = 0
                  for card in self.cards:
                        if isinstance(self.evaluate_map[card], list):
                              total += min(self.evaluate_map[card])
                        else:
                              total += self.evaluate_map[card]

            return total

      def evaluate(self):

            total = self._calculate()      
            self.total_value = total    

            if self.total_value >= 21:

                  self.stand_flag = True

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
            self.turn_end = False
            self.end_game = False
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

      def _check_turn_end(self):


            for hand in self.hands:

                  if hand.stand_flag == True:
                        continue
                        hand.cards = []
                  else:
                        return False
            
            return True

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
            if self._check_turn_end():
                  self.turn_end = True

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

      def __init__(self, name):
            self.name = name
            self.hands = [Hand()]
            self.payout = _PAYOUT

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

      def award_winnings(self, player, hand=0):

            players_current_bet = player.hands[hand].current_bet
            total_payout = players_current_bet * self.payout
            player.balance += total_payout
            print('Awarded {}: {}'.format(player.name, total_payout))
            print('Total payout: {}'.format(total_payout))
            print('{}\'s current balance: {}'.format(player.name, player.balance))
      
      def deal(self, players, deck):

            for _ in range(2):

                  for player in players:
                        player.hands[0].cards.append(deck.pop(0))

                  self.hands[0].cards.append(deck.pop(0))

            for player in players:

                  if player.hands[0].evaluate() == 21:

                        print('BLACKJACK for {}!!!!'.format(player.name))
                        self.award_winnings(player)
                        player.turn_end = True
                  
            

      def play(self, deck, hand=0):
            """
            The dealer 'plays' til a it either goes over or it hits a value greater than or equal to 17
            """

            stopping_condition_has_been_hit = False
            while (not stopping_condition_has_been_hit):

                  if self.hands[hand].evaluate() >= 17:
                        stopping_condition_has_been_hit = True
                  else:
                        print('The dealer hit')
                        self.hit(deck, hand)
                        print('The dealer\'s cards: {}'.format(self.hands[hand].cards))
      
      

def generate_deck(num_decks):

      deck = []
      cards_in_deck = 52
      total_cards_in_deck = num_decks * cards_in_deck

      if num_decks <= 0: 
            raise ValueError('The number of cards must be greater than or equal to 1')
      
      amount_of_each = int(total_cards_in_deck/13)

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