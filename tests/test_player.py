import pytest
from engine.classes.Player import Player
from engine.classes.Card import Card


@pytest.fixture
def player():
    return Player(1, "Test Player", 1000)


def test_player_init(player):
    assert player.player_id == 1
    assert player.player_name == "Test Player"
    assert player.starting_stack == 1000
    assert player.current_stack == 1000
    assert player.hand.get_deck_size() == 0
    assert not player.is_active
    assert not player.is_all_in
    assert not player.has_acted


def test_reset_player_for_new_single_game(player):
    player.is_active = True
    player.is_all_in = True
    player.has_acted = True
    player.hand.add_card(Card("A Heart", 14, "H"))

    player.reset_player_for_new_single_game()

    assert player.hand.get_deck_size() == 0
    assert player.is_active
    assert not player.is_all_in
    assert not player.has_acted


def test_receive_card(player):
    player.receive_card(Card("A Heart", 14, "H"))
    player.receive_card(Card("K Spade", 13, "S"))

    assert player.hand.get_deck_size() == 2
    assert (
        str(player.hand)
        == 'Deck([Card(card_name="A Heart",rank=14,suit="H"), Card(card_name="K Spade",rank=13,suit="S")])'
    )

    player.receive_card(Card("Q Diamond", 12, "D"))
    assert player.hand.get_deck_size() == 2


def test_update_is_active(player):
    player.update_is_active(True)
    assert player.is_active

    player.update_is_active(False)
    assert not player.is_active


def test_bet(player):
    with pytest.raises(ValueError):
        player.bet(100)

    player.is_active = True
    player.bet(100)
    assert player.current_stack == 900
    assert player.has_acted

    with pytest.raises(ValueError):
        player.bet(1000)


def test_active(player):
    player.active()
    assert player.is_active


def test_yet_to_act(player):
    player.has_acted = True
    player.yet_to_act()
    assert not player.has_acted


def test_all_in(player):
    with pytest.raises(ValueError):
        player.all_in()

    player.is_active = True
    player.all_in()
    assert player.current_stack == 0
    assert player.is_all_in

    with pytest.raises(ValueError):
        player.all_in()


def test_to_dict(player):
    player_dict = player.to_dict()
    assert player_dict["player_id"] == 1
    assert player_dict["player_name"] == "Test Player"
    assert player_dict["starting_stack"] == 1000
    assert player_dict["current_stack"] == 1000
    assert player_dict["hand"] == "Deck([])"
    assert not player_dict["is_active"]
    assert not player_dict["is_all_in"]
    assert not player_dict["has_acted"]
