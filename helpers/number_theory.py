import math
from helpers.primes import is_prime

def factorial(n):
    """
    Calulates the factorial of a number
    
    Args:
        n: Number to find the factorial of
        
    Returns:
        factorial of n
    """
    f = 1
    for i in range(n):
        f *= (i+1)
    return f

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
        if n % i == 0 and is_prime(i):
            largest = i
    return largest

def all_factors(n):
    """
    Returns all factors of a number n.
    
    Args:
        n: Number to find factors for
        
    Returns:
        List of all factors of n
    """
    factors = []
    for i in range(1, n + 1):
        if n % i == 0:
            factors.append(i)
    return factors

def proper_factors(n):
    """
    Returns all proper factors of a number n (excluding 1 and n).
    
    Args:
        n: Number to find proper factors for
        
    Returns:
        List of proper factors of n
    """
    factors = []
    for i in range(2, n):
        if n % i == 0:
            factors.append(i)
    return factors

def proper_divisors(n):
    """
    Returns all proper divisors of a number n (excluding n itself).
    
    Args:
        n: Number to find proper divisors for
        
    Returns:
        List of proper divisors of n
    """
    factors = []
    for i in range(1, n):
        if n % i == 0:
            factors.append(i)
    return factors

def is_perfect(n):
    """
    Checks if a number is perfect (sum of proper divisors equals the number).
    
    Args:
        n: Number to check
        
    Returns:
        True if n is perfect, False otherwise
    """
    tmp = proper_divisors(n)
    total = sum(tmp)
    return total == n

def is_abundant(n):
    """
    Checks if a number is abundant (sum of proper divisors exceeds the number).
    
    Args:
        n: Number to check
        
    Returns:
        True if n is abundant, False otherwise
    """
    tmp = proper_divisors(n)
    total = sum(tmp)
    return total > n

def is_deficient(n):
    """
    Checks if a number is deficient (sum of proper divisors is less than the number).
    
    Args:
        n: Number to check
        
    Returns:
        True if n is deficient, False otherwise
    """
    tmp = proper_divisors(n)
    total = sum(tmp)
    return total < n

def is_triangular(n):
    """
    Checks if a number is triangular.
    
    Args:
        n: Number to check
        
    Returns:
        True if n is triangular, False otherwise
    """
    triangular_sum = 0
    for i in range(1, n + 1):
        triangular_sum += i
        if triangular_sum == n:
            return True
        if triangular_sum > n:
            return False
    return False

def is_pentagonal(n):
    """
    Checks if a number is pentagonal.
    
    Args:
        n: Number to check
        
    Returns:
        True if n is pentagonal, False otherwise
    """
    return (1 + (24 * n + 1)**0.5) % 6 == 0

def is_hexagonal(n):
    """
    Checks if a number is hexagonal.
    
    Args:
        n: Number to check
        
    Returns:
        True if n is hexagonal, False otherwise
    """
    return (1 + (8 * n + 1)**0.5) % 4 == 0

def is_pandigital(n, b, z):
    """
    Checks if a number is pandigital in a given base.
    
    Args:
        n: Number to check
        b: Base to check against (if 0, uses length of digits)
        z: Whether to include zero as a digit
        
    Returns:
        True if n is pandigital, False otherwise
    """
    digits = list(set(str(n)))
    a = 0 if z else 1
    base = b if b > 0 else len(digits)
    
    for i in range(a, base + 1):
        if digits.count(str(i)) != 1:
            return False
    return True

def is_curious(n):
    """
    Checks if a number is equal to the sum of the factorials of its digits
    
    Args:
        n: Number to check
        
    Returns:
        True if n is curious, False otherwise
    """
    if sum(factorial(int(str(n)[i])) for i in range(len(str(n)))) == n:
        return True
    return False

def is_circular(n): 
    """
    Checks if all numbers created by permutating a numbers digits, are prime
    
    Args:
        n: Number to check
        
    Returns:
        True if n is circular, False otherwise
    """  
    l = len(str(n))
    rotated_string = str(n)
    
    for i in range(l):
        first_letter = rotated_string[0 : 1] 
        remaining_chars = rotated_string[1 :] 
        rotated_string = remaining_chars + first_letter
        if not is_prime(int(rotated_string)):
            return False
            break
    return True