from words import OneWord, TwoWords, Register
from common import ascii_to_edsac, edsac_to_letter


class EDSAC:
    def __init__(self):
        # 35bits word * 512
        self.memory = [TwoWords()for i in range(512)]
        # 71bits accumulator
        self.accumulator = Register()
        # 35bits multiplier
        self.multiplier = TwoWords()
        self.cards = []
        self.next_char = 0
        self.next_index = 0

    def get_multipiler(self, wide=False):
        if wide:
            return self.multiplier
        return self.multiplier.high

    def set_multipiler(self, value, wide):
        if wide:
            self.multiplier = value
        else:
            self.multiplier.high = value

    def display_multipiler(self):
        print("RS:", self.multiplier)

    def get_memory(self, addr, wide=False):
        is_high = addr % 2
        word = self.memory[addr // 2]
        if wide:
            return word
        else:
            if is_high:
                return word.high
            else:
                return word.low

    def set_memory(self, addr, value, wide=False):
        if wide:
            self.memory[addr // 2] = value
        else:
            is_high = addr % 2
            w = self.memory[addr // 2]
            if is_high:
                w.high = value
            else:
                w.low = value

    def display_memory(self):
        which = 0
        for i in range(34):
            if which == 0:
                print("memory[", i, "]", self.memory[i//2].low,
                      "[", self.memory[i//2].low.as_order(), "]")
            else:
                print("memory[", i, "]", self.memory[i//2].high,
                      "[", self.memory[i//2].high.as_order(), "]")
            which = which ^ 1

    def clear_accumulator(self):
        self.accumulator.__init__()

    def get_accumulator(self, wide=False):
        if wide:
            return self.accumulator.high
        return self.accumulator.high.high

    def set_accumulator(self, value, wide=False):
        if wide:
            self.accumulator.high = value
        else:
            self.accumulator.high.high = value

    def display_accumulator(self):
        print("ABC:", self.accumulator)

    def load_initial_order(self):
        for i, line in enumerate(open("initial_order.txt")):
            v = OneWord.new_from_string(line)
            print(v.as_order())
            self.set_memory(i, v)

    def set_cards(self, cards):
        self.cards = cards
        self.next_char = 0

    def start(self):
        is_finished = False
        self.next_index = 0
        while not is_finished:
            is_finished = self.step()
            # a = input("continue?>")
            # if a == 'n':
            #     continue
            # elif a == 'q':
            #     break

    def step(self):
        instr = self.get_memory(self.next_index)
        op, addr, sl = instr.as_order()
        # print(self.next_index, ":", op, addr, sl)
        if (op == "P") & (addr == 0) & (sl == "S"):
            return True
        wide = (sl == "L")

        if op == "A":
            m = self.get_memory(addr, wide)
            p = self.get_accumulator(wide)
            self.set_accumulator(p + m, wide)

        elif op == "S":
            m = self.get_memory(addr, wide)
            p = self.get_accumulator(wide)
            self.set_accumulator(p - m, wide)

        elif op == "H":
            m = self.get_memory(addr, wide)
            p = self.get_multipiler(wide)
            self.set_multipiler(p + m, wide)

        elif op == "V":
            m = self.get_memory(addr, wide)
            r = self.get_multipiler(wide)
            v = m * r
            if wide:
                a = self.accumulator  # ABC
            else:
                a = self.get_accumulator(wide=True)  # AB
# self.set_accumulator(a + v, wide=True)
            a.set(a + v)

        elif op == "N":
            m = self.get_memory(addr, wide)
            r = self.get_multipiler(wide)
            v = m * r
            if wide:
                a = self.accumulator
            else:
                a = self.get_accumulator(wide=True)
            a.set(a - v)

        elif op == "T":
            a = self.get_accumulator(wide)
            self.set_memory(addr, a, wide)
            self.clear_accumulator()

        elif op == "U":
            a = self.get_accumulator(wide)
            self.set_memory(addr, a, wide)

        elif op == "C":
            raise RuntimeError("Invalid opecode")

        elif op == "R":
            count = 1
            while instr.bits[17 - count] == 0:
                count += 1
            a = self.accumulator.as_int()
            a = a >> count
            self.accumulator.set_from_decimal(a)

        elif op == "L":
            count = 1
            while instr.bits[17 - count] == 0:
                count += 1
            a = self.accumulator.as_int()
            a = a << count
            self.accumulator.set_from_decimal(a)

        elif op == "E":  # A >= 0 goto n
            a = self.get_accumulator(wide)
            if a.bits[0] == 0:
                self.next_index = addr - 1

        elif op == "G":  # A < 0 goto n
            a = self.get_accumulator(wide)
            if a.bits[0] == 1:
                self.next_index = addr - 1

        elif op == "I":
            c = self.cards[self.next_char]
            self.next_char += 1
            v = ascii_to_edsac(c)
            self.set_memory(addr, OneWord.new_from_decimal(v))

        elif op == "O":
            c = self.get_memory(addr)
            print(edsac_to_letter(c.get_charcode()))

        elif op == "F":
            raise RuntimeError("Invalid opecode")

        elif op == "X":
            pass

        elif op == "Y":
            raise RuntimeError("Invalid opecode")

        elif op == "Z":
            return True

        elif op == "P":
            pass

        else:
            raise RuntimeError("Nothing to do")

        self.next_index += 1

        # self.display_accumulator()
        # self.display_multipiler()
        # self.display_memory()

        return False


def main():
    edsac = EDSAC()
    edsac.load_initial_order()
    cards = ["T", "3", "4", "S", "O", "8", "S", "Z", "S"]
    edsac.set_cards(cards)
    edsac.start()


if __name__ == "__main__":
    main()
