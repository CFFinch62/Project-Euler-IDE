def is_palindrome(s):
    """
    Checks if a string is a palindrome.
    
    Args:
        s: String to check
        
    Returns:
        True if s is a palindrome, False otherwise
    """
    return s == s[::-1]

def ltr_to_int(ltr):
    """
    Converts a letter to its position in the alphabet (A=1, B=2, etc.).
    
    Args:
        ltr: Letter to convert
        
    Returns:
        Position of the letter in the alphabet
    """
    l = { 'A' : 1, 'B' : 2, 'C' : 3, 'D' : 4, 'E' : 5, 'F' : 6,
          'G' : 7, 'H' : 8, 'I' : 9, 'J' : 10, 'K' : 11, 'L' : 12,
          'M' : 13, 'N' : 14, 'O' : 15, 'P' : 16, 'Q' : 17, 'R' : 18,
          'S' : 19, 'T' : 20, 'U' : 21, 'V' : 22, 'W' : 23, 'X' : 24,
          'Y' : 25, 'Z' : 26 }
    return l[ltr]

def int_to_ltr(num):
    """
    Converts a number to its corresponding letter in the alphabet (1=A, 2=B, etc.).
    
    Args:
        num: Number to convert (1-26)
        
    Returns:
        Corresponding letter in the alphabet
    """
    i = { 1 : 'A', 2 : 'B', 3 : 'C', 4 : 'D', 5 : 'E', 6 : 'F', 7 : 'G',
          8 : 'H', 9 : 'I', 10 : 'J', 11 : 'K', 12 : 'L', 13 : 'M', 14 : 'N',
          15 : 'O', 16 : 'P', 17 : 'Q', 18 : 'R', 19 : 'S', 20 : 'T', 21 : 'U',
          22 : 'V', 23 : 'W', 24 : 'X', 25 : 'Y', 26 : 'Z'}
    return i[num]

def word_score(w):
    """
    Calculates the score of a word by summing the positions of its letters.
    
    Args:
        w: Word to score
        
    Returns:
        Sum of letter positions in the alphabet
    """
    score = 0
    for i in range(len(w)):
        score += ltr_to_int(w[i])
    return score 