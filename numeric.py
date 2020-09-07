class Value:
    def derive(self, against):
        raise NotImplementedError

    def simplify(self):
        raise NotImplementedError

    def evaluate(self):
        raise NotImplementedError

class Number(Value):
    def __init__(self, name):
        self.name = name

    def derive(self, against):
        if self.name == against:
            return Number(1)
        return Number(0)

    def evaluate(self):
        return self.name

    def simplify(self):
        return self

    def __eq__(self, other):
        if isinstance(other, int):
            return self.name == other
        return self.name == other.name

    def __str__(self):
        return str(self.name)

class Operator(Value):
    pass

class Multiply(Operator):
    def __init__(self, x, y):
        self.name = "*"
        self.x = x
        self.y = y
        self.xs = [x, y]

    def evaluate(self):
        res = 1
        for x in self.xs:
            res *= x.evaluate()

    def derive(self, against):
        return Add(Multiply(self.x, self.y.derive(against)),
                   Multiply(self.x.derive(against), self.y))

    def __eq__(self, other):
        if isinstance(other, Multiply) and self.name == other.name:
            return self.x == other.x and self.y == other.y
        return False


    def simplify(self):
        x = self.x.simplify()
        y = self.y.simplify()

        if x == 0 or y == 0:
            return Number(0)

        if x == 1:
            return y
        if y == 1:
            return x

        return Multiply(x, y)

    def __str__(self):
        return f"(* {self.x} {self.y})"

class Add(Operator):
    def __init__(self, x, y):
        self.name = "+"
        self.x = x
        self.y = y
        self.xs = [x, y]

    def evaluate(self):
        res = 0
        for x in self.xs:
            res += x.evaluate()

    def derive(self, against):
        return Add(self.x.derive(against), self.y.derive(against))

    def __eq__(self, other):
        if isinstance(other, Add) and self.name == other.name:
            return self.x == other.x and self.y == other.y
        return False


    def simplify(self):
        x = self.x.simplify()
        y = self.y.simplify()

        if x == 0:
            return y
        if y == 0:
            return x

        if x == y:
            return Multiply(2, x)

        return Add(x, y)

    def __str__(self):
        return f"(+ {self.x} {self.y})"


x2 = Multiply(Number("x"), Multiply(Number("x"), Number("y")))
print(x2.derive("y").simplify())
