import json
import os
from pathlib import Path

class TemplatesManager:
    def __init__(self):
        self.templates_dir = Path("templates")
        self.templates_dir.mkdir(exist_ok=True)
        self.templates_file = self.templates_dir / "templates.json"
        self.user_templates_file = self.templates_dir / "user_templates.json"
        self.initialize_default_templates()
        self.initialize_user_templates()

    def initialize_default_templates(self):
        """Initialize default templates if they don't exist."""
        if not self.templates_file.exists():
            default_templates = {
                "basic_structure": {
                    "name": "Basic Problem Structure",
                    "description": "Basic template for Project Euler problems",
                    "code": '''"""
Project Euler Problem {problem_number}
"""

def solve():
    """
    Your solution goes here.
    This function should return the answer to the problem.
    """
    # Your code here
    return None

if __name__ == "__main__":
    print(solve())
'''
                },
                "prime_numbers": {
                    "name": "Prime Number Generator",
                    "description": "Efficient prime number generator using Sieve of Eratosthenes",
                    "code": '''def generate_primes(limit):
    """
    Generate all prime numbers up to limit using Sieve of Eratosthenes.
    Returns a list of primes.
    """
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    
    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = [False] * len(sieve[i*i::i])
    
    return [i for i, is_prime in enumerate(sieve) if is_prime]
'''
                },
                "fibonacci": {
                    "name": "Fibonacci Sequence",
                    "description": "Efficient Fibonacci number generator",
                    "code": '''def fibonacci(n):
    """
    Generate the nth Fibonacci number using dynamic programming.
    """
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
'''
                },
                "gcd_lcm": {
                    "name": "GCD and LCM",
                    "description": "Greatest Common Divisor and Least Common Multiple",
                    "code": '''def gcd(a, b):
    """
    Calculate Greatest Common Divisor using Euclidean algorithm.
    """
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    """
    Calculate Least Common Multiple using GCD.
    """
    return a * b // gcd(a, b)
'''
                },
                "pandigital": {
                    "name": "Pandigital Number Checker",
                    "description": "Check if a number is pandigital (contains all digits 1-9 exactly once)",
                    "code": '''def is_pandigital(n, start=1, end=9):
    """
    Check if a number is pandigital (contains all digits from start to end exactly once).
    """
    s = str(n)
    return len(s) == end - start + 1 and set(s) == set(str(i) for i in range(start, end + 1))
'''
                },
                "palindrome": {
                    "name": "Palindrome Checker",
                    "description": "Check if a number or string is a palindrome",
                    "code": '''def is_palindrome(n):
    """
    Check if a number or string is a palindrome.
    """
    s = str(n)
    return s == s[::-1]
'''
                },
                "digit_sum": {
                    "name": "Digit Sum Calculator",
                    "description": "Calculate the sum of digits in a number",
                    "code": '''def digit_sum(n):
    """
    Calculate the sum of digits in a number.
    """
    return sum(int(d) for d in str(n))
'''
                },
                "factorial": {
                    "name": "Factorial Calculator",
                    "description": "Calculate factorial of a number",
                    "code": '''def factorial(n):
    """
    Calculate factorial of a number using iterative approach.
    """
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
'''
                },
                "divisors": {
                    "name": "Divisors Calculator",
                    "description": "Find all divisors of a number",
                    "code": '''def get_divisors(n):
    """
    Find all divisors of a number.
    Returns a sorted list of divisors.
    """
    divisors = set()
    for i in range(1, int(n ** 0.5) + 1):
        if n % i == 0:
            divisors.add(i)
            divisors.add(n // i)
    return sorted(divisors)
'''
                },
                "prime_factors": {
                    "name": "Prime Factorization",
                    "description": "Find prime factors of a number",
                    "code": '''def prime_factors(n):
    """
    Find prime factors of a number.
    Returns a dictionary of prime factors and their exponents.
    """
    factors = {}
    # Handle 2 separately
    while n % 2 == 0:
        factors[2] = factors.get(2, 0) + 1
        n //= 2
    
    # Check odd numbers up to sqrt(n)
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors[i] = factors.get(i, 0) + 1
            n //= i
        i += 2
    
    # If n is a prime > 2
    if n > 2:
        factors[n] = 1
    
    return factors
'''
                },
                "pythagorean_triples": {
                    "name": "Pythagorean Triples Generator",
                    "description": "Generate primitive Pythagorean triples",
                    "code": '''def generate_pythagorean_triples(limit):
    """
    Generate primitive Pythagorean triples where a + b + c <= limit.
    Returns a list of (a, b, c) tuples.
    """
    triples = []
    for m in range(2, int((limit/2)**0.5) + 1):
        for n in range(1, m):
            if (m - n) % 2 == 1 and gcd(m, n) == 1:
                a = m*m - n*n
                b = 2*m*n
                c = m*m + n*n
                if a + b + c <= limit:
                    triples.append((a, b, c))
    return triples
'''
                },
                "combinatorics": {
                    "name": "Combinatorics Functions",
                    "description": "Common combinatorics functions (combinations, permutations)",
                    "code": '''def combinations(n, k):
    """
    Calculate number of combinations (n choose k).
    """
    if k > n:
        return 0
    result = 1
    for i in range(1, k + 1):
        result = result * (n - k + i) // i
    return result

def permutations(n, k):
    """
    Calculate number of permutations (n P k).
    """
    if k > n:
        return 0
    result = 1
    for i in range(n - k + 1, n + 1):
        result *= i
    return result
'''
                }
            }
            self.save_templates(default_templates)

    def initialize_user_templates(self):
        """Initialize user templates file if it doesn't exist."""
        if not self.user_templates_file.exists():
            self.save_user_templates({})

    def save_templates(self, templates):
        """Save default templates to JSON file."""
        with open(self.templates_file, 'w') as f:
            json.dump(templates, f, indent=4)

    def save_user_templates(self, templates):
        """Save user templates to JSON file."""
        with open(self.user_templates_file, 'w') as f:
            json.dump(templates, f, indent=4)

    def load_templates(self):
        """Load all templates (both default and user)."""
        templates = {}
        
        # Load default templates
        if self.templates_file.exists():
            with open(self.templates_file, 'r') as f:
                templates.update(json.load(f))
        
        # Load user templates
        if self.user_templates_file.exists():
            with open(self.user_templates_file, 'r') as f:
                user_templates = json.load(f)
                # Prefix user template keys to avoid conflicts
                for key, value in user_templates.items():
                    templates[f"user_{key}"] = value
        
        return templates

    def get_template(self, template_name):
        """Get a specific template by name."""
        templates = self.load_templates()
        return templates.get(template_name)

    def add_user_template(self, name, template_data):
        """Add a new user template."""
        # Load existing user templates
        user_templates = {}
        if self.user_templates_file.exists():
            with open(self.user_templates_file, 'r') as f:
                user_templates = json.load(f)
        
        # Add new template
        user_templates[name] = template_data
        self.save_user_templates(user_templates)

    def delete_user_template(self, template_name):
        """Delete a user template."""
        if not template_name.startswith("user_"):
            return False
            
        # Load existing user templates
        user_templates = {}
        if self.user_templates_file.exists():
            with open(self.user_templates_file, 'r') as f:
                user_templates = json.load(f)
        
        # Remove the template
        base_name = template_name[5:]  # Remove "user_" prefix
        if base_name in user_templates:
            del user_templates[base_name]
            self.save_user_templates(user_templates)
            return True
        return False 