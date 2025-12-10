#!/usr/bin/env python3
"""
Example: Fibonacci Function
Created by AI Dev Team Demo
"""

def fibonacci(n):
    """
    Calculate the nth Fibonacci number.
    
    Args:
        n (int): The position in the Fibonacci sequence
        
    Returns:
        int: The nth Fibonacci number
        
    Examples:
        >>> fibonacci(0)
        0
        >>> fibonacci(1)
        1
        >>> fibonacci(10)
        55
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci_iterative(n):
    """
    Calculate the nth Fibonacci number iteratively (more efficient).
    
    Args:
        n (int): The position in the Fibonacci sequence
        
    Returns:
        int: The nth Fibonacci number
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


if __name__ == "__main__":
    # Test the functions
    print("Fibonacci Sequence (first 15 numbers):")
    for i in range(15):
        print(f"F({i}) = {fibonacci_iterative(i)}")
    
    # Timing comparison
    import time
    
    n = 30
    
    # Iterative
    start = time.time()
    result = fibonacci_iterative(n)
    iterative_time = time.time() - start
    
    print(f"\nFibonacci({n}) = {result}")
    print(f"Iterative time: {iterative_time:.6f} seconds")
