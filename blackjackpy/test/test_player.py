import pytest
from blackjackpy import app


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


def test_instance_player(player_without_balance):
    player = player_without_balance
    assert isinstance(player, app.Player)


def test_player_pot_default(player_without_balance):
    player = player_without_balance
    assert player.balance == 0


def test_player_pot_instantiation(player_with_balance):
    player = player_with_balance
    assert player.balance == 100


def test_player_bet_action(player_with_balance):
    player = player_with_balance
    player.bet(5)
    assert player.balance == 100 - 5 and player.hands[0].current_bet == 5


def test_player_cards_in_hand(player_with_balance):
    import numpy as np
    player = player_with_balance
    player.cards_in_hand = np.array(['K', '10'])
    assert player.cards_in_hand.size == 2


def test_player_hit(deck, player_with_balance, hand=0):
    player = player_with_balance
    player.hands[hand].hit(deck)
    assert len(player.hands[hand].cards) == 1


def test_player_hit_on_empty_deck(empty_deck, player_with_balance, hand=0):
    player = player_with_balance
    deck = empty_deck
    with pytest.raises(ValueError):
        player.hands[hand].hit(deck)

def test_player_stand(player_with_balance, hand=0):
    player = player_with_balance
    player.stand(hand)
    assert player.turn_end == True

def test_player_split_too_little_cards(player_with_balance, hand=0):
    
    player = player_with_balance
    current_hand = player.hands[hand]
    player.bet(10)
    current_hand.cards = ['10']

    with pytest.raises(ValueError):
        player.split()

def test_player_split_not_enough_balance(player_with_balance, hand=0):
    
    player = player_with_balance
    current_hand = player.hands[hand]
    player.bet(100)
    current_hand.cards = ['10', '10']

    with pytest.raises(ValueError):
        player.split()

def test_player_split_not_equal_cards(player_with_balance, hand=0):
    
    player = player_with_balance
    current_hand = player.hands[hand]
    player.bet(100)
    current_hand.cards = ['K', '10']

    with pytest.raises(ValueError):
        player.split()

def test_player_hit_after_split(player_with_balance, deck, hand=0):

    player = player_with_balance
    current_hand = player.hands[hand]
    player.bet(10)
    current_hand.cards = ['10', '10']
    player.split()
    player.hit(deck)
    assert (len(player.hands[hand].cards) == 2)

def test_player_surrender(player_with_balance, hand=0):

    player = player_with_balance
    previous_balance = player.balance
    current_hand = player.hands[hand]

    player.bet(10)
    current_bet = current_hand.current_bet

    player.surrender(hand)

    assert (player.balance == previous_balance - current_bet / 2)

def test_player_surrender_without_bet(player_with_balance, hand=0):

    player = player_with_balance
    current_hand = player.hands[hand]

    current_hand.cards = ['K', '2', '3']

    with pytest.raises(RuntimeError):
        player.surrender(hand)

def test_player_double_down(player_with_balance, deck, hand=0):

    player = player_with_balance
    current_hand = player.hands[hand]

    current_hand.cards = ['K', '2', '3']
    current_hand.bet(10)
    previous_bet = current_hand.current_bet
    player.double_down(deck, hand)

    assert ((current_hand.current_bet == previous_bet * 2) and
           (len(current_hand.cards) == 4))

def test_player_double_down_with_no_bet(player_with_balance, deck, hand=0):

    player = player_with_balance
    current_hand = player.hands[hand]

    current_hand.cards = ['K', '2', '3']

    with pytest.raises(RuntimeError):
        player.double_down(deck, hand)

def test_player_evaluate(player_with_balance, deck, hand=0):
    
    player = player_with_balance
    current_hand = player.hands[hand]

    current_hand.cards = ['K', '10']
    current_hand_score = current_hand.evaluate()

    assert (current_hand_score == 20)

def test_player_evaluate_edge(player_with_balance, hand=0):

    player = player_with_balance
    current_hand = player.hands[hand]

    current_hand.cards = ['A', 'A', '8']
    current_hand_score = current_hand.evaluate()

    assert current_hand_score == 20

def test_player_split_function(player_with_balance):
    
    player = player_with_balance
    
    player.hands[0].cards = ['2', '2']

    player.split()

    assert len(player.hands) == 2

def test_player_split_then_bet(player_with_balance):

    player = player_with_balance
    player.hands[0].cards = ['2', '2']

    deck = ['K', '9', '3', 'K']

    player.split()

    player.hit(deck, hand=0)
    player.hit(deck, hand=0)
    player.stand(hand=0)

    player.hit(deck, hand=1)
    player.hit(deck, hand=1)

    assert player.hands[1].cards == ['2', '3', 'K']

def test_player_evaluate_edge_with_ace(player_with_balance):

    player = player_with_balance
    player.hands[0].cards = ['2', 'A', '2', '3', '5']

    assert player.hands[0].evaluate() == 13

