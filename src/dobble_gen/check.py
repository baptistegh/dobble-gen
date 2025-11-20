import math


def is_prime(n: int) -> bool:
    """Check if a number is prime.

    Uses an optimized algorithm that checks divisibility by 2 and then
    only odd numbers up to the square root of n.

    Args:
        n: The number to check for primality.

    Returns:
        True if n is a prime number, False otherwise.
    """
    if n % 2 == 0 and n > 2:
        return False
    return all(n % i for i in range(3, int(math.sqrt(n)) + 1, 2))
