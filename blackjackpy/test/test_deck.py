import pytest
from blackjackpy import app
import numpy as np


def build_deck():
    num_cards = 52
    deck = app.generate_deck(num_cards)
    return deck
        
def test_raises():
    with pytest.raises(ValueError):
        deck = app.generate_deck(100)

def test_type():
    deck = app.generate_deck(52)
    assert(isinstance(deck, list))

def test_length():
    num_cards = 52
    deck = app.generate_deck(num_cards)
    assert(len(deck) == num_cards)

def test_unqiue():
    num_cards = 52

    deck = app.generate_deck(num_cards)
    unique_vals = set(deck)
    assert(len(unique_vals) == 13)

      
      

