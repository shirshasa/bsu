# ---- Private arithmetic functions ----
# Returns x + y modulo 2^16. Inputs and output are uint16. Only used by _crypt().


def _add(x, y):
    assert 0 <= x <= 0xFFFF
    assert 0 <= y <= 0xFFFF
    return (x + y) & 0xFFFF


# Returns x * y modulo (2^16 + 1), where 0x0000 is treated as 0x10000.
# Inputs and output are uint16. Note that 2^16 + 1 is prime. Only used by _crypt().
def _multiply(x, y):
    assert 0 <= x <= 0xFFFF
    assert 0 <= y <= 0xFFFF
    if x == 0x0000:
        x = 0x10000
    if y == 0x0000:
        y = 0x10000
    z = (x * y) % 0x10001
    if z == 0x10000:
        z = 0x0000
    assert 0 <= z <= 0xFFFF
    return z


# Returns the additive inverse of x modulo 2^16.
# Input and output are uint16. Only used by _invert_key_schedule().
def _negate(x):
    assert 0 <= x <= 0xFFFF
    return (-x) & 0xFFFF


# Returns the multiplicative inverse of x modulo (2^16 + 1), where 0x0000 is
# treated as 0x10000. Input and output are uint16. Only used by _invert_key_schedule().
def _reciprocal(x):
    assert 0 <= x <= 0xFFFF
    if x == 0:
        return 0
    else:
        return pow(x, 0xFFFF, 0x10001)  # By Fermat's little theorem


class Idea:
    """
    :param: key:  binary array 16-element
    """
    def __init__(self, key):
        assert isinstance(key, list) and len(key) == 16
        self._NUM_ROUNDS = 8
        self.key_schedule = self._expand_key_schedule(key)
        self.inverted_key = self._invert_key_schedule(self.key_schedule)

    def encrypt(self, block, print_debug=False):
        """
        :param: block:8-element bytelist
        :param: key: 16-element byte list
        :return: new 8-element bytelist.
        """
        return self._crypt(block, "encrypt", print_debug)

    def decrypt(self, block, print_debug=False):
        """
        :param: block:8-element bytelist
        :param: key: 16-element byte list
        :return: new 8-element bytelist.
        """
        return self._crypt(block, "decrypt", print_debug)

    # ---- Private cipher functions ----

    def _crypt(self, block, direction, print_debug):
        # Check input arguments
        assert isinstance(block, list) and len(block) == 8
        assert direction in ("encrypt", "decrypt")
        if print_debug:
            print("idea cipher.{}(block = {}, key = {})")

        key_schedule = self.key_schedule
        if direction == "decrypt":
            key_schedule = self.inverted_key

        # Pack block bytes into variables as uint16 in big endian
        w = block[0] << 8 | block[1]
        x = block[2] << 8 | block[3]
        y = block[4] << 8 | block[5]
        z = block[6] << 8 | block[7]

        # Perform 8 rounds of encryption/decryption
        for i in range(self._NUM_ROUNDS):
            if print_debug:
                print("    Round {}: block = [{:04X} {:04X} {:04X} {:04X}]".format(i, w, x, y, z))
            j = i * 6
            w = _multiply(w, key_schedule[j + 0])
            x = _add(x, key_schedule[j + 1])
            y = _add(y, key_schedule[j + 2])
            z = _multiply(z, key_schedule[j + 3])
            u = _multiply(w ^ y, key_schedule[j + 4])
            v = _multiply(_add(x ^ z, u), key_schedule[j + 5])
            u = _add(u, v)
            w ^= v
            x ^= u
            y ^= v
            z ^= u
            x, y = y, x

        # Perform final half-round
        if print_debug:
            print("    Round {}: block = [{:04X} {:04X} {:04X} {:04X}]".format(self._NUM_ROUNDS, w, x, y, z))
        x, y = y, x
        w = _multiply(w, key_schedule[-4])
        x = _add(x, key_schedule[-3])
        y = _add(y, key_schedule[-2])
        z = _multiply(z, key_schedule[-1])

        # Serialize the final block as a byte list in big endian
        return [
            w >> 8, w & 0xFF,
            x >> 8, x & 0xFF,
            y >> 8, y & 0xFF,
            z >> 8, z & 0xFF]

    def _expand_key_schedule(self, key):
        """
        :param key:16-element byte list
        :return: a tuple containing 52 elements of uint16
        """
        # Pack all key bytes into a single uint128
        big_key = 0
        for b in key:
            assert 0 <= b <= 0xFF
            big_key = (big_key << 8) | b
        assert 0 <= big_key < (1 << 128)

        # Append the 16-bit prefix onto the suffix to yield a uint144
        big_key = (big_key << 16) | (big_key >> 112)

        # Extract consecutive 16 bits at different offsets to form the key schedule
        result = []
        for i in range(self._NUM_ROUNDS * 6 + 4):
            offset = (i * 16 + i // 8 * 25) % 128
            result.append((big_key >> (128 - offset)) & 0xFFFF)

        return tuple(result)

    def _invert_key_schedule(self, key_sch):
        """
        :param key_sch: encryption key schedule
        :return:decryption key schedule as a tuple containing 52 elements of uint16
        """
        assert isinstance(key_sch, tuple) and len(key_sch) % 6 == 4
        result = [_reciprocal(key_sch[-4]),
                  _negate(key_sch[-3]),
                  _negate(key_sch[-2]),
                  _reciprocal(key_sch[-1]),
                  key_sch[-6],
                  key_sch[-5]]

        for i in range(1, self._NUM_ROUNDS):
            j = i * 6
            result.append(_reciprocal(key_sch[-j - 4]))
            result.append(_negate(key_sch[-j - 2]))
            result.append(_negate(key_sch[-j - 3]))
            result.append(_reciprocal(key_sch[-j - 1]))
            result.append(key_sch[-j - 6])
            result.append(key_sch[-j - 5])

        result.append(_reciprocal(key_sch[0]))
        result.append(_negate(key_sch[1]))
        result.append(_negate(key_sch[2]))
        result.append(_reciprocal(key_sch[3]))
        return tuple(result)
