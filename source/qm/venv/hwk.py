import itertools
import math
import operator
import re

given = "[p ∧ (q → r)] → (q → r)"

class LogicExpression:
    def __init__(self, statement):
        global brackets
        global operators
        self.statement = re.sub("\\s+", "", statement)
        self.truthtable = {}
        self.predicates = []

        operators = [
            {"u": '\u007e', "p": 2, "f": operator.__not__},
            {"u": '\u2228', "p": 1, "f": operator.__or__},
            {"u": '\u2227', "p": 1, "f": operator.__and__},
            {"u": '\u2194', "p": 0, "f": lambda a, b: int(not (a ^ b))},
            {"u": '\u2192', "p": 0, "f": lambda a, b: int(not a or b)},
        ]
        brackets = {
            "l": ['{', '(', '['],
            "r": ['}', ')', ']']
        }
        try:
            self.evaluate()
        except:
            self.statement = "INVALID STATEMENT"

    def evaluate(self):
        # start truth table by adding in predicates and possible combos
        self.predicates = list(set([c for c in self.statement if c.isalpha()]))
        bincombos = list(itertools.product([0, 1], repeat=len(self.predicates)))
        for x in range(len(self.predicates)):
            self.truthtable[self.predicates[x]] = [b[x] for b in bincombos]

        result = []
        operands = []
        postfix = self.postfix()

        # evaluate until all intermediary steps are in truth table
        for p in postfix:
            if p.isalpha():
                operands.append(p)
            elif any(op['u'] == p for op in operators):
                v0 = operands.pop()
                v1 = operands.pop()
                vals = zip(self.truthtable[v1], self.truthtable[v0])
                op = next(i for i, d in enumerate(operators) if d['u'] == p)

                result = [operators[op]["f"](i, j) for (i, j) in vals]

                substatement = "(" + v1 + str(p) + v0 + ")"

                if substatement not in self.truthtable.keys():
                    self.truthtable[substatement] = result
                operands.append(substatement)

        # add in final given statement to truth table
        self.statement = operands.pop()
        self.truthtable[self.statement] = result

    def postfix(self):
        postfix = []
        ops = []

        for c in self.statement:
            if c.isalpha():
                postfix.append(c)
            elif c in brackets["l"]:
                ops.append(c)
            elif c in brackets["r"]:
                temp = ops.pop()
                while temp not in brackets["l"]:
                    postfix.append(temp)
                    temp = ops.pop()
            elif any(op['u']==c for op in operators):
                while len(ops) and \
                        ops[-1] not in brackets["l"] and \
                        operator.get(ops[-1]['u'], int("inf")) >= operators[c]["p"]:
                    postfix.append(ops.pop())
                ops.append(c)
            else:
                raise SyntaxError

        while len(ops):
            postfix.append(ops.pop())
        return "".join(postfix)

    def display(self):
        for k in self.truthtable.keys():
            print(k, self.truthtable[k])

    @staticmethod
    def combine(a, b):
        if a == b or LogicExpression.diffcount(a, b) != 1:
            return None
        return ''.join([a[i] if a[i] == b[i] else "X" for i in range(len(a))])

    @staticmethod
    def diffcount(a, b):
        check = lambda a, b: a != b and not (a == "X" or b == "X")
        return len([i for i in range(len(a)) if check(a[i], b[i])])

    def simplify(self):
        test = set(self.truthtable[self.statement])
        if len(test) == 1:
            return "T" if test.pop() else "F"

        terms = set(self.minterms())
        simplified = False
        removed = set()
        combined = set()
        previous_size = len(terms)

        while not simplified:
            for x in terms:
                for y in terms:
                    z = LogicExpression.combine(x, y)
                    if z != None:
                        removed.add(x)
                        removed.add(y)
                        combined.add(z)
            for r in removed:
                terms.remove(r)
            for c in combined:
                terms.add(c)
            simplified = len(removed) == 0
            removed.clear()
            combined.clear()

        return self.terms_to_string(terms)

    def terms_to_string(self, terms):
        s = ''
        for t in terms:
            temp = ''
            for i, b in enumerate(t):
                if b == "0":
                    temp += "~" + self.predicates[i]
                if b == "1":
                    temp += self.predicates[i]
            if s != '':
                s += " + " + temp
            else:
                s = temp
        return s

    def minterms(self, n=None):
        m = []
        if n == None:
            m = [i for i, x in enumerate(self.truthtable[self.statement]) if x == 1]
        else:
            m = [i for i in range(2**n)]

        if len(m) > 0:
            size = str(math.ceil(math.log(len(m), 2)))
            m = [format(x, "0" + size + "b") for x in m]
        else:
            m = ["0", "1"]

        return m

    def display(self):
        if self.statement == "INVALID STATEMENT":
            print(self.statement)
        elif len(self.statement) > 1:
            self.prettyprint()
        else:
            print("Statement:", self.statement)
            print("Only one bit value")

    def prettyprint(self):
        print()
        print("Statement:", self.statement)
        print("Simplified:", self.simplify())
        print("Truth Table:")
        longest = len(self.statement)
        for k in self.truthtable.keys():
            difference = " " * (longest - len(k)) + "\t"
            if k != self.statement:
                difference += "\t"

            print(k, "=", end=difference)

            for x in self.truthtable[k]:
                print(x, end=" ")
            print()

if __name__ == "__main__":
    print("Logic Simplifier Tool\n" +
          "Enter a logic expression below.\n" +
          "Valid symbols: ∧, →, ↔, ~, ∨ " +
          "(, {, [, ], }, )\n" +
          "Enter an Expression...")
    given = LogicExpression(input(">> "))
    given.display()
