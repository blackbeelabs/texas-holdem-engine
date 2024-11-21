import pytest
from engine.classes.Card import Card, VALID_CARDS


@pytest.mark.parametrize(
    "card_name,rank,suit",
    [(card_name, rank, suit) for card_name, (rank, suit) in VALID_CARDS],
)
def test_card_creation(card_name, rank, suit):
    card = Card(card_name, rank, suit)
    assert card.verbose_name == card_name
    assert card.rank == rank
    assert card.suit == suit


@pytest.mark.parametrize(
    "card_name,rank,suit",
    [(card_name, rank, suit) for card_name, (rank, suit) in VALID_CARDS],
)
def test_card_to_dict(card_name, rank, suit):
    card = Card(card_name, rank, suit)
    card_dict = card.to_dict()
    assert card_dict["card_name"] == card_name
    assert card_dict["rank"] == rank
    assert card_dict["suit"] == suit


@pytest.mark.parametrize(
    "card_name,rank,suit",
    [(card_name, rank, suit) for card_name, (rank, suit) in VALID_CARDS],
)
def test_card_str_representation(card_name, rank, suit):
    card = Card(card_name, rank, suit)
    expected_str = (
        f"Card({{'card_name': '{card_name}', 'rank': {rank}, 'suit': '{suit}'}})"
    )
    assert str(card) == expected_str
