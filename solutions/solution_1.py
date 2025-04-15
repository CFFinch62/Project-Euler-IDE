M1 = 3
M2 = 5
LIMIT = 1000

def solve():
    return sum_of_two_multiples(M1, M2, LIMIT)

def sum_of_two_multiples(m1, m2, limit):
    sum = 0
    for num in range(limit):
        if (num % m1 == 0 or num % m2 == 0):
            sum += num      
    return sum

# Expected sum 233168 

