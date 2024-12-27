#!/usr/bin/env python3

def load_input(filename):
    secrets = []
    with open(filename) as f:
        for line in f:
            secrets.append(int(line))
    return secrets


def compute_next(secret, n=1):
    for i in range(n):
        secret = ((secret & 0x03ffff) << 6) ^ secret
        secret = (secret >> 5) ^ secret
        secret = ((secret & 0x001fff) << 11 ) ^ secret
    return secret


def compute_all(secrets, n=1):
    return sum(compute_next(s, n) for s in secrets)


def get_prices(secret, n):
    d = secret % 10
    for i in range(n):
        secret = compute_next(secret)
        next_d = secret % 10
        yield (next_d, next_d - d)
        d = next_d


def analyze_prices(secret, n):
    first = {}
    price = get_prices(secret, n)
    (_, a) = next(price)
    (_, b) = next(price)
    (_, c) = next(price)
    for (p, d) in price:
        if (a, b, c, d) not in first:
            first[(a, b, c, d)] = p
        (a, b, c) = (b, c, d)
    return first


def compute_payout(secrets, n):
    total = {}
    for secret in secrets:
        for (changes, price) in analyze_prices(secret, n).items():
            if changes not in total:
                total[changes] = price
            else:
                total[changes] += price
    max_payout = None
    best_tracker = None
    for (changes, payout) in total.items():
        if max_payout is None or payout > max_payout:
            max_payout = payout
            best_tracker = changes
    return best_tracker, max_payout



secrets = load_input('input.txt')
#secrets = [1, 10, 100, 2024]
#secrets = [1, 2, 3, 2024]

#s = 123
#for i in range(10):
#    s = compute_next(s)
#    print(s)

#analyze_prices(123, 10)
#print(compute_payout([123], 10))


print('AOC 2024 22 part 1')
print(compute_all(secrets, 2000))

print()

print('AOC 2024 22 part 2')
print(compute_payout(secrets, 2000))




