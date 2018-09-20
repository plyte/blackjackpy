import pytest
from blackjackpy import app, view

@pytest.fixture
def instantiate_dealer():
    dealer = app.Dealer('Jack')
    return dealer

@pytest.fixture
def deck():
    from blackjackpy import app
    num_cards = 52
    deck = app.generate_deck(num_cards)
    return deck

def test_dealer_hit_stopping_condition(instantiate_dealer, deck, hand=0):

    dealer = instantiate_dealer

    dealer.hands[hand].cards = ['K', 'A']
    
    with pytest.raises(RuntimeError):
        dealer.hit(deck=deck, hand=hand)
    
def test_dealer_playing_hit_till_stopping_condition(instantiate_dealer, hand=0):

    dealer = instantiate_dealer
    dealer.hands[hand].cards = ['K', '2']

    deck = ['3', '2', 'K']

    dealer.play(deck)

    assert dealer.hands[hand].total_value == 17

def test_dealer_playing_hit_check(instantiate_dealer, hand=0):

    dealer = instantiate_dealer
    dealer.hands[hand].cards = ['K', 'A']

    deck = ['1']

    dealer.play(deck)

    assert dealer.hands[hand].total_value == 21

def test_dealer_player_hit_goes_over(instantiate_dealer, hand=0):

    dealer = instantiate_dealer
    dealer.hands[hand].cards = ['K', '6']

    deck = ['K']

    dealer.play(deck)

    assert dealer.hands[hand].total_value == 26

def test_dealer_player_hit_check_condition_with_aces(instantiate_dealer, hand=0):

    dealer = instantiate_dealer
    dealer.hands[hand].cards = ['A', '6']

    deck = ['K', 'K']

    dealer.play(deck)

    assert dealer.hands[hand].total_value == 17