import random

def dec_to_bin(n):
    """
    Converts a decimal number to binary.
    
    Args:
        n: Decimal number to convert
        
    Returns:
        Binary string representation
    """
    return bin(n).replace("0b", "")

def rnd_bin_str(n):
    """
    Generates a random binary string of length n.
    
    Args:
        n: Length of the binary string
        
    Returns:
        Random binary string
    """
    bin_str = ""
    for i in range(n):
        bin_str += str(random.randint(0, 1))
    return bin_str

def sum_digits(n):
    """
    Calculates the sum of digits in a number.
    
    Args:
        n: Number to sum digits of
        
    Returns:
        Sum of digits
    """
    idx = 0
    sum = 0
    snum = str(n)
    while idx < len(snum):
        sum = sum + int(snum[idx])
        idx += 1
    return sum 