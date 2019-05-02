from itertools import product
from typing import Callable
from sys import stdout
import inspect


def build_truth_table(func: Callable, with_argnames: bool = False) -> list:
    """*args, **kwargs - bool args"""
    assert callable(func)
    init_table = product([False, True], repeat=func.__code__.co_argcount)

    final_table = [(*r, func(*r)) for r in init_table]
    if with_argnames:
        final_table.insert(
            0, (*inspect.getfullargspec(func).args, func.__code__.co_name)
        )
    return final_table


def print_table(table: list, padding: int = 2):
    max_lengths = [0] * len(table[0])
    for row in table:
        for i, v in enumerate(row):
            max_lengths[i] = max(max_lengths[i], len(str(v)))

    separator_row = "+" + "+".join("-" * (l + padding * 2) for l in max_lengths) + "+"
    for row in table:
        print(separator_row)
        for i, v in enumerate(row):
            stdout.write(f"|{v:^{max_lengths[i] + padding * 2}}")
        stdout.write("|\n")
    print(separator_row)


if __name__ == "__main__":
    import pprint
    import inspect

    def test(x, y, z=0):
        return x and y or z

    print_table(build_truth_table(test, with_argnames=True))
