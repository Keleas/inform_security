import random

from math import gcd

from src.tools import is_prime, generate_large_prime


def loop_is_prime(number):
    # looping to reduce probability of rabin miller false +
    is_number_prime = True
    for i in range(0, 20):
        is_number_prime *= is_prime(number)
        if not is_number_prime:
            return is_number_prime
    return is_number_prime


def modexp(base, exp, modulus):
    return pow(base, exp, modulus)


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


def key_generation():
    print("Computing key values, please wait...")
    loop = True
    while loop:
        k = random.randrange(2 ** 415, 2 ** 416)  # 416 bits
        q = generate_large_prime(160)
        p = (k * q) + 1
        while not (is_prime(p)):
            k = random.randrange(2 ** 415, 2 ** 416)  # 416 bits
            q = generate_large_prime(160)
            p = (k * q) + 1
        L = p.bit_length()
        """
        g=t^(p-1)/q  %  p
        if(g^q  % p = 1) we found g
        """

        t = random.randint(1, p - 1)
        g = square_multiply(t, (p - 1) // q, p)

        if 512 <= L <= 1024 and \
                L % 64 == 0 and \
                gcd(p - 1, q) > 1 \
                and square_multiply(g, q, p) == 1:
            loop = False

            a = random.randint(2, q - 1)
            h = square_multiply(g, a, p)
            print("p = ", p)
            print("q = ", q)
            print("g = ", g)
            print("h = ", h)
            print("a = ", a)

            file1 = open("data/key.txt", "w")
            file1.write(str(p))
            file1.write("\n")
            file1.write(str(q))
            file1.write("\n")
            file1.write(str(g))
            file1.write("\n")
            file1.write(str(h))
            file1.close()

            file2 = open("data/secret_key.txt", "w")
            file2.write(str(a))
            file2.close()

            print("Verification key stored at data/key.txt and secret key stored at data/secret_key.txt")
