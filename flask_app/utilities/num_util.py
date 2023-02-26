def test_valid_floating_point(num_str):
    # stringing string methods together to check for valid number
    #
    # .strip() remove whitespace
    # .lstrip('-') remove a leading '-' in case of negative number
    # .replace('.') remove 1 and only 1 '.' if decimal
    # .isdigit() returns True if all characters are 1-9
    is_num_valid = num_str.strip().lstrip('-').replace('.', '', 1).isdigit()

    return is_num_valid