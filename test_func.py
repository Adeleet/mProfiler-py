from mProfiler import mProfiler
from string import ascii_letters
from random import choice, randint

profiler = mProfiler()


def rand_str(l=5, h=30):
    """
    Returns a random ASCII string between 'l' and 'h' length
    """
    return "".join([choice(ascii_letters) for i in range(randint(l, h))])


def test_func():
    profiler.start_breakpoint("init_array")
    str_array = [rand_str() for i in range(1000)]
    profiler.start_breakpoint("lengths")
    str_lengths = [len(s) for s in str_array]
    profiler.start_breakpoint("mean_length")
    mean_length = sum(str_lengths)/len(str_lengths)
    profiler.end()


test_func()
