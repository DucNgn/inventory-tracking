import string
import random


def generate_random_string() -> str:
    length = 5
    letters = string.ascii_uppercase
    return "".join(random.choice(letters) for i in range(length))
