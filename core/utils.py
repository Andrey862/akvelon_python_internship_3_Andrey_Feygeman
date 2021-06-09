def fibonacci(n: int) -> int:
    """
        returns Nth fibonacci number
    """
    if (n < 0):
        raise ValueError('n must be greater or equal to 0')
    if (n == 0):
        return 0
    a, b = 0, 1
    for _ in range(n-1):
        a, b = b, a+b
    return b
