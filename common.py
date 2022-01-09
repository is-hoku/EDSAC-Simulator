def int_to_bits(n, width):  # 10進数の n を width bit の配列に2進数(2の補数表現)に変換
    w = bin(2**width - 1)
    b = bin(n & int(w, 2))
    length = len(b) - 2
    binary = []
    for i in range(length):
        binary.insert(0, int(b[i+2]))
    result = [0] * (width - len(binary))
    binary.reverse()
    result.extend(binary)
    return result


def bits_to_int(bits):  # 2進数(2の補数表現)のビット配列を int に変換
    result = 0
    for i in bits[1:]:
        result *= 2
        result += i
    result -= bits[0] * (2 ** (len(bits) - 1))
    return result


LETTERS = 'PQWERTYUIOJ#SZK*.F@D!HNM&LXGABCV'
FIGURES = '0123456789?#"+(*,$@;!L,.&)/#-?:='


def ascii_to_edsac(c):  # 文字を EDSAC での文字コードに変換
    r = LETTERS.find(c)
    if r == -1:
        r = FIGURES.find(c)
        if r == -1:
            print("Error: invalid character %c", c)
    return r


def edsac_to_letter(c):
    return LETTERS[c]


def edsac_to_figure(c):
    return FIGURES[c]
