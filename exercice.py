#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import deque

from time import perf_counter_ns


def params(*args, **kwargs):
    txt = "("
    txtArgs = [str(arg) for arg in args]
    txtArgs += [f"{key}={value}" for key, value in kwargs.items()]
    txt += ", ".join(txtArgs) + ")"
    return txt


def printElapsed(func):
    def argWrapper(*args, **kwargs):
        t1 = perf_counter_ns()
        ret = func(*args, **kwargs)
        print(f"{func.__name__}{params(*args)} -> {ret} in "
              + f"{(perf_counter_ns() - t1) / 1e6:.3e}ms")
        return ret

    return argWrapper


@printElapsed
def dynamicFibonacci(n): return fibonacci(n)

@printElapsed
def naiveFibonacci(n): return get_fibonacci_number(n)

def fibonacci(n, cache={0: 0, 1: 1}):
    """Faster fibonacci"""
    cached = cache.get(n, None)
    if cached is not None: # careful, cached may be 0 -> false
        return cached
    else:
        cache[n] = fibonacci(n-2, cache) + fibonacci(n-1, cache)
        return cache[n]


def get_fibonacci_number(n):
    return get_fibonacci_number(n-2) + get_fibonacci_number(n-1) if n > 1 else n


def get_fibonacci_sequence(n):
    sequence = [0, 1]
    for i in range(n - 2):
        sequence.append(sequence[i] + sequence[i+1])

    return sequence[0:n]


def get_sorted_dict_by_decimals(d):
    return {key: val for key, val in sorted(list(zip(d.keys(), d.values())), key=lambda x: x[1]%1)}


def fibonacci_numbers(length):
    previous = [0, 1]
    current = 0

    while current < 2:
        yield previous[current]
        current += 1

    while current < length:
        nextt = previous[0] + previous[1]
        previous[0] = previous[1]
        previous[1] = nextt
        current += 1
        yield nextt


def build_recursive_sequence_generator(initialValues, func, cacheAllValues = False):
    def innerSmallMemory(length):
        vals = initialValues.copy() # avoid mutable weirdness
        current = 0

        while current < len(vals):
            yield vals[current]
            current += 1 

        while current < length:
            nextt = func(vals)
            for i in range(1, len(vals)):
                vals[i-1] = vals[i]
            vals[-1] = nextt
            yield nextt
            current += 1

    def innerBigMemory(length):
        vals = initialValues.copy() # avoid mutable weirdness
        current = 0

        while current < len(vals):
            yield vals[current]
            current += 1 

        while current < length:
            nextt = func(vals)
            vals.append(nextt)
            yield nextt
            current += 1

    return innerBigMemory if cacheAllValues else innerSmallMemory


if __name__ == "__main__":
    for i in range(10, 11950, 50):
        dynamicFibonacci(i)
        # naiveFibonacci(i)
        print()


    print([get_fibonacci_number(0), get_fibonacci_number(1), get_fibonacci_number(2)])
    print([get_fibonacci_number(i) for i in range(10)])
    print()

    print(get_fibonacci_sequence(1))
    print(get_fibonacci_sequence(2))
    print(get_fibonacci_sequence(10))
    print()

    spam = {
        2: 2.1,
        3: 3.3,
        1: 1.4,
        4: 4.2
    }
    eggs = {
        "foo": 42.6942,
        "bar": 42.9000,
        "qux": 69.4269,
        "yeet": 420.1337
    }
    print(get_sorted_dict_by_decimals(spam))
    print(get_sorted_dict_by_decimals(eggs))
    print()

    for fibo_num in fibonacci_numbers(10):
        print(fibo_num, end=" ")
    print("\n")

    def fibo_def(last_elems):
        return last_elems[-1] + last_elems[-2]
    fibo = build_recursive_sequence_generator([0, 1], fibo_def)
    for fi in fibo(10):
        print(fi, end=" ")
    print("\n")

    lucas = build_recursive_sequence_generator([2, 1], lambda x: sum(x))
    print(f"Lucas : {[elem for elem in lucas(10)]}")

    def prod(x):
        res = 1
        for coeff in x:
            res *= coeff
        return res

    perrin = build_recursive_sequence_generator([3, 0, 2], lambda x: x[-2]+x[-3])
    print(f"Perrin : {[elem for elem in perrin(10)]}")

    hofstadter_q = build_recursive_sequence_generator([1, 1], lambda x: x[len(x) - x[-1]] + x[len(x) - x[-2]], True)
    print(f"Hofstadter-Q : {[elem for elem in hofstadter_q(10)]}")
