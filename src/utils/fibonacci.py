# original idea was a recursive function, but was very slow
# changed for generator as it allows to go a bit beyond

cache = {}

# fibonacci generator function
def fibonacci_gen(fib1: int=1, fib2: int=1):
    yield fib1
    while True:
        fib1, fib2 = fib2, fib1 + fib2
        yield fib2

def get_fibonacci(n: int, fibIdx: int=1) -> int:
    try:
        if not type(n) == int: n = int(n)
        if n in cache: return cache[n]
        fibonacci, result = fibonacci_gen(), 0

        # add to cache for faster look ups while service is running
        # in terms of lambda this migth not benefit much due to concurrency and cold starts
        # TODO persist cache to a file and read when loading program
        while (fibIdx < n):
            fibIdx += 1
            result: int = next(fibonacci)
            cache[fibIdx] = result

    except:
        return 0
    return result