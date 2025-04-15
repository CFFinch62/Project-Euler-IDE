def hamming_weight(x: int) -> int:
    """
    Returns the number of 1's in the binary representation of a non-negative integer.
    
    Args:
        x: Non-negative integer
        
    Returns:
        Number of 1's in the binary representation of x
    """
    return bin(x).count("1") 