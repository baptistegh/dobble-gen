from dobble_gen import check
from dobble_gen.config import nb_cards
from dobble_gen.generator import dobble_combinations


def test_combinations():
    def check_dobble(i, cards) -> bool:
        print(f"Testing {i} symbols per cards")
        for i in range(len(cards)):
            for j in range(i + 1, len(cards)):
                inter = set(cards[i]) & set(cards[j])
                if len(inter) != 1:
                    return False
        return True

    for i in range(30):
        if check.is_prime(i - 1):
            cards = dobble_combinations(i, nb_cards(i))
            assert check_dobble(i, cards)
