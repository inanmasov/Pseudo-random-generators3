def gen(s, p):
    new_bit = 0
    for i in range(0, len(p)):
        new_bit += s[i] * p[i]
    new_bit %= 2
    out_bit = s[len(s) - 1]
    s = [new_bit] + s[:len(s) - 1]
    return out_bit, s


def generate(s, L, p):
    sequence = []
    for i in range(L):
        new_s, s = gen(s, p)
        sequence.append(new_s)

    return sequence


def start_stop(L):
    d = 3
    sequences = []

    count1 = 0
    for i in range(d):
        # p = int(input("Введите p для " + str(i+1) + " генератора: "))
        p = 124657
        p = [int(a) for a in bin(p)[3:]]
        s = int(input("Введите s для " + str(i+1) + " генератора: "))
        s = [int(bit) for bit in bin(s)[2:]]
        s = [0] * (len(p) - len(s)) + s

        if i == 0:
            tmp_sec = generate(s, L, p)
            for j in tmp_sec:
                count1 += j
            sequences.append(generate(s, L, p))
        elif i == 1:
            sequences.append(generate(s, count1 + 1, p))
        elif i == 2:
            sequences.append(generate(s, L - count1 + 1, p))

    g = []
    sec2 = 0
    sec3 = 0
    for i in range(len(sequences[0])):
        g.append((sequences[1][sec2] + sequences[2][sec3]) % 2)
        if sequences[0][i] == 1:
            sec2 += 1
        else:
            sec3 += 1
    print(g)
    return g

def bytes_to_bits(bytes_data):
    return ''.join(format(byte, '08b') for byte in bytes_data)

def bits_to_bytes(bits_string):
    bytes_list = [int(bits_string[i:i+8], 2) for i in range(0, len(bits_string), 8)]
    return bytes(bytes_list)

def decrypt_file():
    with open("encrypted.txt", 'rb') as file:
        data = bytes_to_bits(file.read())

    g = start_stop(len(data))
    out = ''
    for i in range(len(data)):
        out += str((int(data[i]) + g[i]) % 2)

    with open("decrypted.txt", 'wb') as file:
        file.write(bits_to_bytes(out))

def encrypt_file():
    with open("text.txt", 'rb') as file:
        binary_data = file.read()

    bin = bytes_to_bits(binary_data)
    g = start_stop(len(bin))

    out = ''
    for i in range(len(bin)):
        out += str((int(bin[i]) + g[i]) % 2)

    with open("encrypted.txt", 'wb') as file:
        file.write(bits_to_bytes(out))


mode = int(input("Введите 1 (П-1) или 2 (П-2): "))
if mode == 1:
    L = int(input("Введите L: "))
    start_stop(L)
elif mode == 2:
    f = int(input("Введите 1 (Зашифровать) или 2 (Расшифровать): "))
    if f == 1:
        encrypt_file()
    elif f == 2:
        decrypt_file()