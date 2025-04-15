# Helper Files Guide

Helper files are a powerful feature that allows you to organize your code and create reusable functions for Project Euler problems. This guide explains how to create, edit, and use helper files effectively.

## Creating Helper Files

1. Click the "Add Helper File" button
2. Enter a filename (e.g., `helpers.py`, `math_utils.py`, etc.)
3. The file will be created with a template including:
   - A docstring with the problem number
   - An example function with documentation
   - Comments guiding where to add more functions

## Basic Example

Here's a simple example of a helper file (`helpers.py`) with two related functions:

```python
"""
Helper functions for Project Euler Problem 3
"""

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
```

## Using Helper Functions

You can use helper functions in your main solution in several ways:

### 1. Import Specific Functions
```python
from helpers import is_prime, gpf

def solve():
    number = 600851475143
    if is_prime(number):
        return number
    return gpf(number)
```

### 2. Import with Aliases
```python
from helpers import is_prime as check_prime, gpf as greatest_prime_factor

def solve():
    number = 600851475143
    if check_prime(number):
        return number
    return greatest_prime_factor(number)
```

### 3. Import the Entire Module
```python
import helpers

def solve():
    number = 600851475143
    if helpers.is_prime(number):
        return number
    return helpers.gpf(number)
```

## Helper Files Working Together

Helper files can import from each other. For example, you could split the above functions into two files:

`primes.py`:
```python
def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
```

`factors.py`:
```python
from primes import is_prime

def gpf(n):
    """Find the greatest prime factor of a number."""
    largest = 1
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0 and is_prime(i):
            largest = i
    return largest
```

Then in your solution:
```python
from factors import gpf

def solve():
    number = 600851475143
    return gpf(number)  # This will still use is_prime from primes.py
```

## Testing Helper Functions

You can test your helper functions using the "Test Helper Function" button:

1. Select the helper file containing the function
2. Click "Test Helper Function"
3. Enter the function name
4. Enter arguments in one of these formats:
   - Positional: `1, 2, 'hello'`
   - Keyword: `x=1, y=2, name='test'`
   - Mixed: `1, 2, name='test'`

## Best Practices

1. **Organization**: Group related functions together in helper files
2. **Documentation**: Include docstrings explaining what each function does
3. **Naming**: Use clear, descriptive names for functions and files
4. **Testing**: Test helper functions independently before using them in your solution
5. **Reusability**: Write helper functions to be reusable across different problems

## Common Use Cases

1. **Mathematical Functions**:
   - Prime number checks
   - Greatest common divisor
   - Factorial calculations
   - Number theory utilities

2. **String Operations**:
   - Palindrome checks
   - String permutations
   - Character counting

3. **Data Structures**:
   - Custom data structures
   - Tree/graph operations
   - Sorting algorithms

4. **File Operations**:
   - Data file parsing
   - Input validation
   - Output formatting

Remember: Helper files are there to make your life easier. Use them to organize your code and avoid repeating common operations across different problems. 