import math

def combine(a, b):
    if a == b or diffcount(a, b) != 1:
        return None
    return ''.join([a[i] if a[i] == b[i] else "X" for i in range(len(a))])

def diffcount(a, b):
    check = lambda a, b: a != b and not (a == "X" or b == "X")
    return len([i for i in range(len(a)) if check(a[i], b[i])])

def minterms(n=0):
    """
    Returns a list of string formatted minterms. This will be
    all possible 2^n combinations or the minterms for which
    this logic statement is true.

    :param n: possible number of predicates in statement
    :return: minterms: a list of minterms formatted in a string
    """
    minterms = []
    if False:
        minterms = [i for i, x in enumerate(self.truthtable[self.statement]) if x == 1]
    else:
        minterms = [i for i in range(2**n)]

    bitsize = str(math.ceil(math.log(len(minterms), 2)))
    minterms = [format(x, "0" + bitsize + "b") for x in minterms]

    return minterms

m = minterms(3)
s = False
terms = set(m)
p = len(terms)
r = set()
n = set()

while not s:
    for x in terms:
        for y in terms:
            z = combine(x, y)
            if z != None:
                r.add(x)
                r.add(y)
                n.add(z)
    for v in r:
        terms.remove(v)
    for u in n:
        terms.add(u)
    s = len(r) == 0
    r.clear()
    n.clear()

print(m, "=", terms)