import math


def is_prime(n):
    """
    Check if number is a prime.

    :param n: number to be checked
    """
    if n % 2 == 0 and n > 2:
        return False
    return all(n % i for i in range(3, int(math.sqrt(n)) + 1, 2))
