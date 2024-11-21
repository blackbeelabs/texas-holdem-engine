import pytest
from engine.classes.Deck import Deck
from engine.classes.Card import Card


def test_init_default():
    deck = Deck()
    assert deck.get_deck_size() == 52
    assert not deck.empty()


def test_init_do_not_shuffle():
    deck = Deck(do_not_shuffle=True)
    assert deck.get_deck_size() == 52
    print([str(card) for card in deck.cards])
    assert deck.cards[0].verbose_name == "2-Club"
    assert deck.cards[-1].verbose_name == "A-Spade"


def test_init_empty_deck():
    deck = Deck(new_deck=False)
    assert deck.get_deck_size() == 0
    assert deck.empty()


def test_shuffle():
    deck = Deck(do_not_shuffle=True)
    original_order = deck._get_cards_as_list()
    deck._shuffle()
    assert deck._get_cards_as_list() != original_order


def test_deal():
    deck = Deck()
    card = deck.deal()
    assert isinstance(card, Card)
    assert deck.get_deck_size() == 51


def test_deal_empty_deck():
    deck = Deck(new_deck=False)
    with pytest.raises(ValueError, match="No cards remaining in the deck"):
        deck.deal()


def test_add_card():
    deck = Deck(new_deck=False)
    card = Card("2-Club", "2", "C")
    deck.add_card(card)
    assert deck.get_deck_size() == 1
    assert str(deck.cards[0].verbose_name) == "2-Club"


def test_empty():
    deck = Deck()
    assert not deck.empty()
    while not deck.empty():
        deck.deal()
    assert deck.empty()


def test_get_deck_size():
    deck = Deck()
    assert deck.get_deck_size() == 52
    deck.deal()
    assert deck.get_deck_size() == 51
