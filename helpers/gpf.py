import is_prime

def gpf(n):
    """
    Find the greatest prime factor of a number.
    
    Args:
        n: Number to find greatest prime factor of
        
    Returns:
        The greatest prime factor of n
    """
    largest = 1
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0 and is_prime.is_prime(i):
            largest = i
    return largest