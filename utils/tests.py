def are_equal(actual, expected):
    try:
        assert actual == expected
    except:
        print('actual =', actual, 'expected =', expected)
        raise

def generate_test_file(file_name, lines):
    with open(file_name, 'w') as file:
        file.writelines(lines)
