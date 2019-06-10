import random
import string


def random_id(id_length):
    return "".join([random.choice(string.digits + string.ascii_lowercase) for i in range(id_length)])