import common
import re


class Edsac:
    def __init__(self):
        self.memory = 1


class OneWord:  # 17bit words

    bitwidth = 17

    def __init__(self, bits=None):
        if bits:
            print(bits)
            self.bits = bits
        else:
            self.bits = [0] * self.bitwidth

    @staticmethod
    def new_from_decimal(n):
        """
        >>> a = OneWord.new_from_decimal(-255)
        >>> a.bits
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1]
        """
        return OneWord(common.int_to_bits(n, 17))

    def set_from_decimal(self, n):
        """
        >>> a = OneWord.new_from_decimal(-255)
        >>> a.set_from_decimal(47)
        >>> a.bits
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1]
        """
        self.bits = common.int_to_bits(n, 17)
        return self

    def as_int(self):
        """
        >>> a = OneWord.new_from_string("00000000000101111").as_int
        47
        """
        n = common.bits_to_int(self.bits)
        return n

    def as_real(self):
        """
        >>> a = OneWord.new_from_string("11000000000000000").as_real
        -0.5
        """
        return self.as_int() / float(2 ** (self.bitwidth - 1))

    @staticmethod
    def new_from_string(s):
        """
        >>> a = OneWord.new_from_string("00000000000101111")
        >>> a.bits
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1]
        """
        bits = re.findall("[01]", s)
        return OneWord([int(i) for i in bits])

    @staticmethod
    def new_from_order(order):
        """
        >>> a = OneWord.new_from_order(('R', 16, 'S'))
        >>> a.bits
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        """
        op, addr, sl = order
        if sl == 'S':
            sl = [0]
        else:
            sl = [1]
        op_bit = common.int_to_bits(common.ascii_to_edsac(op), 5)
        unused_bit = [0]
        addr_bit = common.int_to_bits(addr, 10)
        result = op_bit + unused_bit + addr_bit + sl
        return OneWord(result)

    def as_order(self):
        """
        >>> a = OneWord.new_from_order(('R', 16, 'S'))
        >>> a.as_order
        ('R', 16, 'S')
        """
        op = common.edsac_to_letter(common.bits_to_int(self.bits[:5]))
        addr = common.bits_to_int(self.bits[6:16])
        sl = 'S' if self.bits[16] == 0 else 'L'
        return (op, addr, sl)

    def __add__(self, v):
        return self.new_from_decimal(self.as_int() + v.as_int())

    def __sub__(self, v):
        return self.new_from_decimal(self.as_int() - v.as_int())

    def __mul__(self, v):
        return self.new_from_decimal((self.as_int() * v.as_int()) << 2)

    def set(self, v):
        self.bits = v.bits
