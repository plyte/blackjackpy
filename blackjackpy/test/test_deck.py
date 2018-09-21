import pytest
from blackjackpy import app
import numpy as np


@pytest.fixture
def build_deck():
    num_decks = 2
    deck = app.generate_deck(num_decks)
    return deck
        
def test_raises():
    with pytest.raises(ValueError):
        deck = app.generate_deck(-1)

def test_type(build_deck):
    deck = build_deck
    assert(isinstance(deck, list))

def test_length(build_deck):
    deck = build_deck
    assert(len(deck) == 52*2)

def test_unqiue(build_deck):
    unique_vals = set(build_deck)
    assert(len(unique_vals) == 13)

def test_shuffle(build_deck):
    from blackjackpy import app
    before_shuffle_deck = build_deck[:]
    after_shuffle_deck = app.shuffle_deck(build_deck)[:]
    assert(before_shuffle_deck != after_shuffle_deck)

def test_pop(build_deck):
    build_deck.pop(0)
    assert(build_deck != 52)
      

