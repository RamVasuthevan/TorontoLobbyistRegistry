def is_postal_code(raw_postal_code: str) -> bool:
    valid_postal_first_third_chars = set("ABCEGHJKLMNPRSTVXY")
    valid_postal_chars = set("ABCEGHJKLMNPRSTVWXYZ")
    valid_digits = set("0123456789")
    valid_white_space = set(" ")

    valid_chars = [
        valid_postal_first_third_chars,  # A
        valid_digits,  # 1
        valid_postal_chars,  # A
        valid_white_space,  # <space>
        valid_digits,  # 1
        valid_postal_chars,  # A
        valid_digits,  # 1
    ]

    if len(raw_postal_code) != len(valid_chars):
        return False

    for char, valid_set in zip(raw_postal_code, valid_chars):
        if char not in valid_set:
            return False

    return True
