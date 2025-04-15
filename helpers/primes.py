def is_prime(n):
    """
    Check if a number is prime.
    
    Args:
        n: Number to check
        
    Returns:
        True if n is prime, False otherwise
    """
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_left_truncatable_prime(n):
    """
    Check if a number is a left truncatable prime.
    
    Args:
        n: Number to check
        
    Returns:
        True if n is left truncatable, False otherwise
    """
    strNum = str(n)
    cnt = 1
    
    if "0" in strNum:
        return False
    
    for i in range(len(strNum) - 1):
        strNum = strNum[1::]
        intNum = int(strNum)
        if is_prime(intNum):
            cnt += 1

    if cnt == len(str(n)):
        return True
    else:
        return False

def is_right_truncatable_prime(n):
    """
    Check if a number is a right truncatable prime.
    
    Args:
        n: Number to check
        
    Returns:
        True if n is right truncatable, False otherwise
    """
    strNum = str(n)
    cnt = 1
    
    if "0" in strNum:
        return False
    
    for i in range(len(strNum) - 1):
        strNum = strNum[:(len(strNum) - 1):]
        intNum = int(strNum)
        if is_prime(intNum):
            cnt += 1
      
    if cnt == len(str(n)):
        return True
    else:
        return False

def get_primes_up_to(n):
    """
    Returns a list of all primes up to n using Sieve of Eratosthenes.
    
    Args:
        n: Upper limit
        
    Returns:
        List of primes up to n
    """
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = [False] * len(sieve[i*i::i])
    return [i for i, is_prime in enumerate(sieve) if is_prime] 