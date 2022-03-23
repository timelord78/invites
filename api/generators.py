import random
import string


def confirm_code():
    code = random.randint(1000, 9999)
    return code


def invite_code():
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = ''.join(random.sample(letters_and_digits, 6))
    return rand_string
