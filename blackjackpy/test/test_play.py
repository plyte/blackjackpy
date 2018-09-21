import pytest
from blackjackpy import app
from blackjackpy import view

'''
What do we want to test:

The player will specify how many players
that many players will be generated

Then the dealer will be generated
and the game will start

The game starts with the players having each a specific balance

Each player bets the minimum and then the game is starded

The game starts by dealing the players one
card faceup and then dealing the dealer one card face down
the dealer then deals the players the remain card face up 
and deals one card face up to the dealer as the last action

The players then each play their turn until they stay

The dealer then hits until their hand equals 17 or higher
Once the dealer either stays or goes over the game is over and the 
bets are returned with odds to the player


'''
@pytest.fixture
def deck():
    from blackjackpy import app
    num_decks = 2
    deck = app.generate_deck(num_decks)
    return deck


@pytest.fixture
def empty_deck():
    deck = []
    return deck


@pytest.fixture
def player_without_balance():
    player = app.Player('Matthew')
    return player


@pytest.fixture
def player_with_balance():
    player = app.Player('Matthew', 100)
    return player

@pytest.fixture
def instantiated_start_of_game():
    dealer = app.Dealer('Jack')
    players = [app.Player('Matthew', 1000), app.Player('John', 1000)]
    return (dealer, players)

def test_start_of_game():

    bj = app.Blackjack(10)
    bj.start()

    assert(bj.start_flag == True)

def test_initialize_players():

    dealer = app.Dealer('Jack')
    num_players = 2
    initial_balance = 1000
    names = ['Matthew', 'John']
    players = []
    for i in range(num_players):
        players.append(app.Player(name=names[i], balance=initial_balance))

    assert(isinstance(players[0], app.Player) and isinstance(players[1], app.Player) 
           and isinstance(dealer, app.Dealer))

def test_deal(instantiated_start_of_game, deck, hand=0):

    dealer = instantiated_start_of_game[0]
    players = instantiated_start_of_game[1]

    deck = app.shuffle_deck(deck)
    dealer.deal(players, deck)

    assert((len(players[0].hands[hand].cards) == 2) and
           (len(players[1].hands[hand].cards) == 2) and
           (len(dealer.hands[hand].cards) == 2))

def test_total_round(instantiated_start_of_game, hand=0):

    dealer = app.Dealer('Dealer')
    players = [app.Player('Matthew', 100)]
    deck = ['K', '10', '4', 'K', 'Q']
    dealer.deal(players, deck)

    current_hand = players[0].hands[hand]

    players[0].bet(10)

    current_hand.cards = []
    current_hand_score = current_hand.evaluate()

    players[0].stand()

    dealer.play(deck)

    assert ((current_hand_score < dealer.hands[hand].evaluate()) and 
            (players[0].turn_end == True))

def test_total_round_player_wins(instantiated_start_of_game, hand=0):

    dealer = app.Dealer('Dealer')
    players = [app.Player('Matthew', 100)]
    deck = ['K', '10', '4', 'K', '7']
    dealer.deal(players, deck)

    current_hand = players[0].hands[hand]

    players[0].bet(10)
    players[0].hit(deck)

    current_hand_score = current_hand.evaluate()

    players[0].stand()
    dealer.play(deck)

    assert ((current_hand_score > dealer.hands[hand].evaluate()) and 
            (players[0].turn_end == True))

def test_dealer_play_round(instantiated_start_of_game, hand=0):

    dealer = instantiated_start_of_game[0]
    players = instantiated_start_of_game[1]

    deck = ['A', 'K', 'Q', '10', 'A', 'A']

    dealer.deal(players=players, deck=deck)

    assert (players[1].turn_end == True)


