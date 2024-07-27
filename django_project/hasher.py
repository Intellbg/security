import hashlib
import string
import random
import time


def salt_generator(
    size=10, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase
):
    return "".join(random.choice(chars) for _ in range(size))


def generate_hash():
    hash = hashlib.sha1()
    hash.update(str(time.time()).encode("utf-8") + salt_generator().encode("utf-8"))
    final_hash = hash.hexdigest()[:-10]
    return final_hash


def generate_hash_email(email):
    hash = hashlib.sha1()
    hash.update(
        str(time.time()).encode("utf-8") + salt_generator().encode("utf-8") + email
    )
    final_hash = hash.hexdigest()[:-10]
    return final_hash
