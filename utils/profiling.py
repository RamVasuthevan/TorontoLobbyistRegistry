from contextlib import contextmanager
import time


@contextmanager
def timer(description: str):
    """
    Context manager for timing a block of code.

    Args:
        description: Description of the code block to be timed.
    """
    start_time = time.time()
    try:
        yield
    finally:
        end_time = time.time()
        print(f"{description}: {end_time - start_time} seconds")
