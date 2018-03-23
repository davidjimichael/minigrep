import operator
import re
import itertools

import math

given = "[p ∧ (q → r)] → (q → r)"
#
# operators = [
#     {"u": '\u007e', "prec": 2, "funct": operator.__not__},
#     {"u": '\u2228', "prec": 1, "funct": operator.__or__},
#     {"u": '\u2227', "prec": 1, "funct": operator.__and__},
#     {"u": '\u2194', "prec": 0, "funct": lambda a, b: int(not (a ^ b))},
#     {"u": '\u2192', "prec": 0, "funct": lambda a, b: int(not a or b)},
# ]
# brackets = {
#     "l": ['{', '(', '['],
#     "r": ['}', ')', ']']
# }




class LogicExpression:
    def __init__(self, statement):
        self.statement = re.sub("\\s+", "", statement)
        self.predicates = list(set([c for c in self.statement if c.isalpha()]))
        self.truthtable = {}
        self.simplified_statement = ""

        self.brackets = ['}', ')', ']', '[', '{', '(']
        self.ops = ['\u007E', '\u2228', '\u2227', '\u2192', '\u2194']

        self.op_props = {
            '\u007E': {"prec": 2, "funct": operator.__not__},
            '\u2228': {"prec": 1, "funct": operator.__or__},
            '\u2227': {"prec": 1, "funct": operator.__and__},
            '\u2192': {"prec": 0, "funct": lambda a, b: int(not a or b)},
            '\u2194': {"prec": 0, "funct": lambda a, b: int(not (a ^ b))},
        }

    def valid(self):
        for c in self.statement:
            if not (c in self.ops or c in self.brackets or c.isalpha()):
                return False
        return True

    def evaluate(self):
        bincombos = list(itertools.product([0, 1], repeat=len(self.predicates)))
        for x in range(len(self.predicates)):
            self.truthtable[self.predicates[x]] = [b[x] for b in bincombos]
        postfix = self.postfix()
        res = []
        operands = []

        for p in postfix:
            if p not in self.ops:
                operands.append(p)
            elif p in self.ops:
                v0 = operands.pop()
                v1 = operands.pop()
                res = [self.op_props[p]["funct"](i, j) for (i, j) in zip(self.truthtable[v1], self.truthtable[v0])]
                substatement = "(" + v1 + str(p) + v0 + ")"
                if substatement not in self.truthtable.keys():
                    self.truthtable[substatement] = res
                operands.append(substatement)
        self.statement = operands.pop()
        self.truthtable[self.statement] = res

    def postfix(self):
        postfix = []
        ops = []
        bracket = {
            "l": ['{', '(', '['],
            "r": ['}', ')', ']']
        }

        for c in self.statement:
            if c.isalpha():
                postfix.append(c)
            elif c in bracket["l"]:
                ops.append(c)
            elif c in bracket["r"]:
                temp = ops.pop()
                while temp not in bracket["l"]:
                    postfix.append(temp)
                    temp = ops.pop()
            elif c in self.ops:
                while len(ops) and ops[-1] not in bracket["l"] and self.op_props.get(ops[-1], int("inf")) >= \
                        self.op_props[c]["prec"]:
                    postfix.append(ops.pop())
                ops.append(c)
            else:
                raise SyntaxError
        #  end for
        while len(ops):
            postfix.append(ops.pop())
        return "".join(postfix)

    def display(self):
        for k in self.truthtable.keys():
            print(k, self.truthtable[k])

    def simplify(self):
        new = set()
        terms = set()
        table = dict()
        removed = set()
        simplified = False
        minterms = self.minterms()
        datasize = int(math.log(len(minterms), 2))

        for i in range(datasize+1):
            table.update({i: [m for m in minterms if m.count("1") == i]})

        for i in range(datasize+1):
            for b in table[i]:
                for p in table[i+1]:



        print(table)
        while not simplified:
            simplified = True

    def combine(self, a, b):
        x = lambda a, b: a != b or a=="X" or b=="X"
        fluxbits = [i for i in range(len(a)) if x(a[i], b[i])]

        if len(fluxbits) == 1:
            return ''.join(["X" if x(a[i], b[i]) else a[i] for i in range(len(a))])
        else:
            return None

    def minterms(self, n=None):
        """
        Returns a list of string formatted minterms. This will be
        all possible 2^n combinations or the minterms for which
        this logic statement is true.

        :param n: possible number of predicates in statement
        :return: minterms: a list of minterms formatted in a string
        """
        minterms = []
        if n == None:
            minterms = [i for i, x in enumerate(self.truthtable[self.statement]) if x == 1]
        else:
            minterms = [i for i in range(2**n)]

        bitsize = str(math.ceil(math.log(len(minterms), 2)))
        minterms = [format(x, "0" + bitsize + "b") for x in minterms]

        return minterms

    # def simplify(self):
    #     # uncomment before later
    #     # test = set(self.truthtable[self.statement])
    #     # if len(test) == 1:
    #     #     return "T" if test.pop() else "F"
    #
    #     minterms = []
    #     terms = set()
    #     #  create minterms list and the counts of the ones in the binary string
    #     for x in range(len(self.truthtable[self.statement])):
    #         if self.truthtable[self.statement][x]:
    #             binstr = format(x, "0"+str(len(self.predicates))+"b")
    #             ones = binstr.count("1")
    #             minterms.append({"binary": binstr, "ones": ones})
    #             terms.add(binstr)
    #
    #     table = dict()
    #     removed = set()
    #     for i in range(len(self.predicates)+1):
    #         table.update({i: [m["binary"] for m in minterms if m["ones"] == i]})
    #
    #     keys = sorted(table.keys())
    #     simplified = False
    #     for v in table.values():
    #         for x in v:
    #             terms.add(x)
    #     count = lambda a, b: len([i for i in range(a) if a[i] != b[i]])
    #
    #     while not simplified:
    #         # for all the min terms
    #         for ki, k in enumerate(keys):
    #             # find next key
    #             nextkey = keys[ki + 1 if ki < len(keys)-1 else ki]
    #             for m in table[k]:
    #                 # reference needed to check comparisons
    #                 count = 0
    #                 # enumerate the minterms
    #                 # for all the bits
    #                 for bi, b in enumerate(m):
    #                     # if they're a 0
    #                     if b == "0":
    #                         # increase comparisons by 1
    #                         count += 1
    #                         # create a possible match to minterm in next set
    #                         match = m[:bi] + '1' + m[bi+1:]
    #                         # if match exists (in next group)
    #                         if match in table[nextkey]:
    #                             # create the combo of these
    #                             dontcare = m[:bi] + "X" + m[bi + 1:]
    #                             # add them both to used set
    #                             print(m, match, dontcare)
    #                             removed.add(m)
    #                             removed.add(match)
    #                             # add new term to newterms set
    #                             terms.add(dontcare)
    #
    #         temp = terms.copy()
    #         # for all combos
    #         for i, d in enumerate(temp):
    #             # for each letter in the combo
    #             for j, c in enumerate(d):
    #                 # if we have a "care" value and another term has a dont care there
    #                 dc = next((x for x in temp if x[j]=="X"), None)
    #                 if not (c == "X" or dc == None):
    #                     # combine the two terms then the combo will be X unless both terms have same value
    #                     # in position at this index or j in this case
    #                     combo = ""
    #                     for k in range(len(d)):
    #                         if ((d[k] == "X" or dc[k] == "X") or d[k] != dc[k]):
    #                             combo += "X"
    #                         else:
    #                             combo += d[k]
    #                     removed.add(d)
    #                     removed.add(dc)
    #                     simplified = False
    #                     terms.add(combo)
    #                     print(d, dc, combo, "terms", terms)
    #
    #     return terms.remove(removed)


if __name__ == "__main__":
    # print("Logic Simplifier Tool\n" +
    #       "Enter a logic expression below.\n" +
    #       "Valid symbols: ∧, →, ↔, ~, ∨ " +
    #       "(, {, [, ], }, )\n" +
    #       "Enter an Expression...")
    # given = LogicExpression(input(">> "))
    given = LogicExpression(given)
    given.evaluate()
    given.display()
    print("valid=", given.valid())
    print("simplified=", given.simplify())

