import common


def _test_common():
    test_args = [47, 0, -32, -255]
    test_args2 = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1],  # 47
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 0
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],  # -32
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1]  # -255
    ]
    print("> common.int_to_bits(n, width)")
    for i in test_args:
        print("input: ", i, "output: ", common.int_to_bits(i, 17))
    print("\n> common.bits_to_int(bits)")
    for i in test_args2:
        print("input: ", i, "output: ", common.bits_to_int(i))


if __name__ == "__main__":
    _test_common()
