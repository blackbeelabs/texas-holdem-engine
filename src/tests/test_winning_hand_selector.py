import pytest
from utils.WinningHandSelector import WinningHandSelector


# Common test data
@pytest.fixture
def valid_hands():
    return {"Player1": ["AS", "KS"], "Player2": ["JH", "JD"]}


@pytest.fixture
def valid_community():
    return ["JS", "JC", "4H", "8D", "2C"]


def test_valid_hands(valid_hands, valid_community):
    assert WinningHandSelector.validate_hands(valid_hands, valid_community) == True


def test_invalid_card_format(valid_community):
    invalid_format_hands = {"Player1": ["ASS", "KS"], "Player2": ["JH", "JD"]}
    with pytest.raises(ValueError, match="Invalid card format"):
        WinningHandSelector.validate_hands(invalid_format_hands, valid_community)


def test_invalid_card_face(valid_community):
    invalid_face_hands = {"Player1": ["XS", "KS"], "Player2": ["JH", "JD"]}
    with pytest.raises(ValueError, match="Invalid card face"):
        WinningHandSelector.validate_hands(invalid_face_hands, valid_community)


def test_invalid_card_suit(valid_community):
    invalid_suit_hands = {"Player1": ["AX", "KS"], "Player2": ["JH", "JD"]}
    with pytest.raises(ValueError, match="Invalid card suit"):
        WinningHandSelector.validate_hands(invalid_suit_hands, valid_community)


def test_duplicate_cards_in_player_hands(valid_community):
    duplicate_player_hands = {
        "Player1": ["AS", "KS"],
        "Player2": ["AS", "JD"],  # AS is duplicated
    }
    with pytest.raises(ValueError, match="Duplicate cards found"):
        WinningHandSelector.validate_hands(duplicate_player_hands, valid_community)


def test_duplicate_cards_with_community(valid_hands):
    duplicate_community = ["AS", "JC", "4H", "8D", "2C"]  # AS is duplicated
    with pytest.raises(ValueError, match="Duplicate cards found"):
        WinningHandSelector.validate_hands(valid_hands, duplicate_community)


def test_wrong_number_of_hole_cards(valid_community):
    wrong_hole_cards = {"Player1": ["AS"], "Player2": ["JH", "JD"]}
    with pytest.raises(ValueError, match="must have exactly 2 hole cards"):
        WinningHandSelector.validate_hands(wrong_hole_cards, valid_community)


def test_wrong_number_of_community_cards(valid_hands):
    # Test with 1 card
    wrong_community_1 = ["2H"]
    with pytest.raises(
        ValueError, match="Number of community cards must be 0, 3, 4, or 5"
    ):
        WinningHandSelector.validate_hands(valid_hands, wrong_community_1)

    # Test with 2 cards
    wrong_community_2 = ["2H", "3H"]
    with pytest.raises(
        ValueError, match="Number of community cards must be 0, 3, 4, or 5"
    ):
        WinningHandSelector.validate_hands(valid_hands, wrong_community_2)

    # Test with 6 cards
    wrong_community_6 = ["2H", "3H", "4H", "5H", "6H", "7H"]
    with pytest.raises(
        ValueError, match="Number of community cards must be 0, 3, 4, or 5"
    ):
        WinningHandSelector.validate_hands(valid_hands, wrong_community_6)
