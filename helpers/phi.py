def phi(n):
    """
    Euler's Totient Function - counts the positive integers up to n that are relatively prime to n.
    
    Args:
        n: Number to calculate totient for
        
    Returns:
        The number of integers less than n that are coprime with n
    """
    # Initialize result as n
    result = n
    # Consider all prime factors of n and subtract their multiples from result
    p = 2
    while p * p <= n:
        # Check if p is a prime factor
        if n % p == 0:
            # If yes, then update n and result
            while n % p == 0:
                n = int(n / p)
            result -= int(result / p)
        p += 1
    # If n has a prime factor greater than sqrt(n)
    if n > 1:
        result -= int(result / n)
    return result 