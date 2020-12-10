import random
import os
import math

from src.sha import sha1


def compute_inverse(in1, in2):
    """
    Compute inverse (using extended Euclidean algorithm
    """
    aL = [in1]
    bL = [in2]
    tL = [0]
    t = 1
    sL = [1]
    s = 0
    q = math.floor((aL[0] / bL[0]))
    r = (aL[0] - (q * bL[0]))

    while r > 0:
        temp = (tL[0] - (q * bL[0]))
        tL[0] = t
        t = temp
        temp = (sL[0] - (q * s))
        sL[0] = s
        s = temp
        aL[0] = bL[0]
        bL[0] = r
        q = math.floor(aL[0] / bL[0])
        r = (aL[0] - (q * bL[0]))

    inverse = s % in2
    return inverse


def square_multiply(x, c, n):
    z = 1
    # getting value of l by converting c into binary representation and getting its length
    c = "{0:b}".format(c)[::-1]  # reversing the binary string

    l = len(c)
    for i in range(l - 1, -1, -1):
        z = pow(z, 2)
        z = z % n
        if c[i] == '1':
            z = (z * x) % n
    return z


def sha_hash(file_name: str):
    """
    Create hash from document by sha1 algorithm.

    :param file_name: str name of document for signature
    :return: int value of hash
    """
    BLOCKSIZE = 65536
    line = ''  # format one line for hash
    with open(file_name, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)  # read each line of doc
        while len(buf) > 0:
            line += buf.decode('utf-8')
            buf = afile.read(BLOCKSIZE)

    hex = "0x" + sha1(line.encode())  # create sha1 hash
    return int(hex, 0)


def sign(file_name: str) -> None:
    """
    Create signature and save it into data/signature.txt

    :param file_name: file name for signature
    :return: None
    """
    print("Signing the file...")
    file_name = os.path.join('data', file_name)

    file1 = open("data/key.txt", "r")
    file2 = open("data/secret_key.txt", "r")
    p = int(file1.readline().rstrip())
    q = int(file1.readline().rstrip())
    g = int(file1.readline().rstrip())
    h = int(file1.readline().rstrip())
    a = int(file2.readline().rstrip())

    loop = True
    while loop:
        r = random.randint(1, q - 1)
        c1 = square_multiply(g, r, p)
        c1 = c1 % q
        c2 = sha_hash(file_name) + (a * c1)
        rinverse = compute_inverse(r, q)
        c2 = (c2 * rinverse) % q

        if c1 != 0 and c2 != 0:
            loop = False

    print('hash = ', sha_hash(file_name))
    print('c1 = ', c1)
    print('c2 = ', c2)
    file = open("data/signature.txt", "w")
    file.write(str(c1))
    file.write("\n")
    file.write(str(c2))
    print("cipher stored at signature.txt")


def verification(file_name: str) -> None:
    """
    Verification process of signature for file name document

    :param file_name: file name for signature verification
    :return: None
    """
    print("Verification process...")
    file_name = os.path.join('data', file_name)

    file1 = open("data/key.txt", "r")
    file2 = open("data/signature.txt", "r")
    p = int(file1.readline().rstrip())
    q = int(file1.readline().rstrip())
    g = int(file1.readline().rstrip())
    h = int(file1.readline().rstrip())

    c1 = int(file2.readline().rstrip())
    c2 = int(file2.readline().rstrip())
    print('c1 = ', c1)
    print('c2 = ', c2)

    t1 = sha_hash(file_name)
    print('hash = ', t1)
    inverseC2 = compute_inverse(c2, q)
    t1 = (t1 * inverseC2) % q

    t2 = compute_inverse(c2, q)
    t2 = (t2 * c1) % q

    valid1 = square_multiply(g, t1, p)
    valid2 = square_multiply(h, t2, p)
    valid = ((valid1 * valid2) % p) % q
    if valid == c1:
        print("Valid signature")
    else:
        print("Invalid signature")
