from dobble_gen import check


def test_is_prime():
    assert check.is_prime(2)
    assert check.is_prime(3)
    assert not check.is_prime(4)
    assert check.is_prime(5)
    assert not check.is_prime(6)
    assert check.is_prime(7)
    assert not check.is_prime(8)
    assert not check.is_prime(9)
    assert not check.is_prime(10)
    assert check.is_prime(11)
    assert not check.is_prime(12)
    assert check.is_prime(13)
    assert not check.is_prime(14)
    assert not check.is_prime(15)
    assert not check.is_prime(16)
    assert check.is_prime(17)
    assert not check.is_prime(18)
