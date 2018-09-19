import pytest
from blackjackpy import app


@pytest.fixture
def deck():
    from blackjackpy import app
    num_cards = 52
    deck = app.generate_deck(num_cards)
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

def test_player_stand(player_with_balance):
    player = player_with_balance
    player.stand()
    assert player.stand_flag == True

def test_player_split_not_enough(player_with_balance, hand=0):
    import numpy as np
    player = player_with_balance
    current_hand = player.hands[hand]
    player.bet(10)
    previous_bet = current_hand.current_bet
    current_hand.cards = ['10']

    with pytest.raises(ValueError):
        player.split()