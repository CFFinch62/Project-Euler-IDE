def gcd(n1, n2):
    """
    Calculates the Greatest Common Divisor of two numbers using Euclidean algorithm.
    
    Args:
        n1: First number
        n2: Second number
        
    Returns:
        Greatest Common Divisor of n1 and n2
    """
    while n2 > 0:
        n1, n2 = n2, n1 % n2
    return n1

def lcm(n1, n2):
    """
    Calculates the Least Common Multiple of two numbers.
    
    Args:
        n1: First number
        n2: Second number
        
    Returns:
        Least Common Multiple of n1 and n2
    """
    return n1 * n2 / gcd(n1, n2) 