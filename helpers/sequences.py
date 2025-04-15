def collatz_chain(n):
    """
    Generates the Collatz chain for a number n.
    
    Args:
        n: Starting number
        
    Returns:
        List of numbers in the Collatz chain
    """
    chain = []
    chain.append(n)
    
    if n % 2 == 0:
        tmp = n // 2
        chain.append(tmp)
        while tmp != 1:
            if tmp % 2 == 0:
                tmp //= 2
                chain.append(tmp)
            else:
                tmp = (3 * tmp) + 1
                chain.append(tmp)
    else:
        tmp = (3 * n) + 1
        chain.append(tmp)
        while tmp != 1:
            if tmp % 2 == 0:
                tmp //= 2
                chain.append(tmp)
            else:
                tmp = (3 * tmp) + 1
                chain.append(tmp)
    
    return chain

def is_lychrel(n):
    """
    Checks if a number is a Lychrel number.
    
    Args:
        n: Number to check
        
    Returns:
        True if n is a Lychrel number, False otherwise
    """
    rn = int(str(n)[::-1])
    nn = n
    i = 0
    while i < 51:
        nn = nn + rn
        if is_palindrome(str(nn)):
            return False
        i += 1
        rn = int(str(nn)[::-1])
    return True

def is_curzon(num):
    """
    Checks if a number is a Curzon number.
    
    Args:
        num: Number to check
        
    Returns:
        True if num is a Curzon number, False otherwise
    """
    elv = 2 ** num + 1
    mul = 2 * num + 1
    res = elv % mul
    return res == 0 