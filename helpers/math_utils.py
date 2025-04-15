import math

def choose(r, d):
    """
    Calculates the binomial coefficient (r choose d).
    
    Args:
        r: Total number of items
        d: Number of items to choose
        
    Returns:
        Binomial coefficient
    """
    return (math.factorial(r) / (math.factorial(d) * math.factorial(r-d)))

def create_integer_set(start, limit):
    """
    Creates a set containing integers from 1 up to the given limit (inclusive).

    Args:
        limit: An integer specifying the upper bound of the set.

    Returns:
        A set containing integers from 1 to limit.
    """
    if not isinstance(limit, int) or limit < 1:
        raise ValueError("Limit must be a positive integer.")
    if not isinstance(start, int) or start < 1:
        raise ValueError("Start must be a positive integer.")
    return set(range(start, limit + 1))

def find_abundant_numbers(limit):
    sum_of_divisors = [0] * (limit + 1) # Initialize an array to store sum of divisors

    for i in range(2, limit + 1): # Iterate through numbers starting from 2
        for j in range(i * 2, limit + 1, i): # Iterate through multiples
            sum_of_divisors[j] += i # Add the divisor to the sum of divisors

    abundant_numbers = []
    for i in range(2, limit + 1): # Check for abundance
        if sum_of_divisors[i] > i:
            abundant_numbers.append(i)

    return abundant_numbers

def pairwise_sums(numbers):
    """
    Generates all possible sums of combinations of 2 numbers from a list.
    This is an efficient implementation that avoids duplicate calculations.
    
    Args:
        numbers: List of numbers to generate pairwise sums from
        
    Returns:
        List of all possible sums of combinations of 2 numbers
    """
    sums = []
    n = len(numbers)
    for i in range(n):
        for j in range(i + 1, n):
            sums.append(numbers[i] + numbers[j])
    return sums

def unique_pairwise_sums(numbers, limit):
    """
    Generates all possible unique sums of combinations of 2 numbers from a list.
    This is an efficient implementation that avoids duplicate calculations.
    
    Args:
        numbers: List of numbers to generate pairwise sums from
        
    Returns:
        Set of all unique sums of combinations of 2 numbers up to limit
    """
    sums = set()
    for num1 in numbers:
        for num2 in numbers:
            if num1 + num2 < limit:
                sums.add(num1 + num2)
    return sums


def is_square(x):
    """
    Checks if a number is a perfect square.
    
    Args:
        x: Number to check
        
    Returns:
        True if x is a perfect square, False otherwise
    """
    if x < 0:
        return False
    y = math.isqrt(x)
    return y * y == x

def is_odd(n):
    """
    Checks if a number is odd.
    
    Args:
        n: Number to check
        
    Returns:
        True if n is odd, False otherwise
    """
    return n % 2 != 0

def progress_bar(progress, total):
    """
    Displays a progress bar.
    
    Args:
        progress: Current progress
        total: Total amount
        
    Returns:
        None (prints progress bar)
    """
    percent = 100 * (progress / float(total))
    bar = 'X' * int(percent) + '-' * (100 - int(percent))
    print(f"\r|{bar}| {percent:.2f}%", end="\r") 