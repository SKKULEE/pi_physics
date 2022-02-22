from math import isnan

class rational:
    def __init__(self, numerator: int = 0, denominator: int = 1):
        self.numerator = numerator
        self.denominator = denominator
        self.normallize()

    def __repr__(self):
        if isnan(self.numerator) or isnan(self.denominator):
            return "nan"
        return "%s%s" % (self.numerator, ("/%s" % self.denominator) if self.denominator != 1 else "")

    def __neg__(self):
        return rational(-self.numerator, self.denominator)

    def __add__(self, oper):
        if type(oper) == rational:
            if isnan(self.numerator) or isnan(oper.numerator) or isnan(self.denominator) or isnan(oper.denominator):
                return rational("nan")
            if self == rational("inf"):
                if oper == -rational("inf"):
                    return rational("nan")
                return rational("inf")
            return rational(self.numerator * oper.denominator + oper.numerator * self.denominator, self.denominator * oper.denominator)
        if type(oper) == int:
            return rational(self.numerator + oper * self.denominator, self.denominator)
        if type(oper) == float:
            return float(self) + oper
        raise TypeError("unsupported operand type(s) for + and -: 'rational' and '%s'" % type(oper))

    def __radd__(self, oper):
        return self + oper

    def __sub__(self, oper):
        return self + (-oper)

    def __rsub__(self, oper):
        return -(self - oper)

    def __mul__(self, oper):
        if type(oper) == rational:
            if isnan(self.numerator) or isnan(oper.numerator) or isnan(self.denominator) or isnan(oper.denominator):
                return rational("nan")
            return rational(self.numerator * oper.numerator, self.denominator * oper.denominator)
        if type(oper) == int:
            return rational(self.numerator * oper, self.denominator)
        if type(oper) == float:
            return float(self) * oper
        raise TypeError("unsupported operand type(s) for *: 'rational' and '%s'" % type(oper))

    def __rmul__(self, oper):
        return self * oper

    def __truediv__(self, oper):
        if type(oper) == rational:
            if isnan(self.numerator) or isnan(oper.numerator) or isnan(self.denominator) or isnan(oper.denominator):
                return rational("nan")
            return rational(self, oper)
        if type(oper) == int:
            return rational(self, oper)
        if type(oper) == float:
            return float(self) / oper
        raise TypeError("unsupported operand type(s) for / and //: 'rational' and '%s'" % type(oper))

    def __rtruediv__(self, oper):
        if type(oper) == int:
            return rational(oper, self)
        if type(oper) == float:
            return oper * float(self.reciprocal())
        raise TypeError("unsupported operand type(s) for / and //: 'rational' and '%s'" % type(oper))

    def __floordiv__(self, oper):
        return rational(int(self / oper))
    
    def __rfloordiv__(self, oper):
        return rational(int(oper / self))

    def __mod__(self, oper):
        if type(oper) == rational:
            if isnan(self.numerator) or isnan(oper.numerator) or isnan(self.denominator) or isnan(oper.denominator):
                return rational("nan")
            return rational((self.numerator * oper.denominator) % (oper.numerator * self.denominator), self.denominator * oper.denominator)
        if type(oper) == int:
            return rational(self.numerator % (oper*self.denominator), self.denominator)
        if type(oper) == float:
            return float(self) % oper
        raise TypeError("unsupported operand type(s) for %: 'rational' and '%s'" % type(oper))

    def __rmod__(self, oper):
        if type(oper) == int:
            return rational((oper*self.denominator) % self.numerator , self.denominator)
        if type(oper) == float:
            return oper % float(self)
        raise TypeError("unsupported operand type(s) for %: 'rational' and '%s'" % type(oper))

    def __pow__(self, oper):
        if type(oper) == rational:
            if isnan(self.numerator) or isnan(oper.numerator) or isnan(self.denominator) or isnan(oper.denominator):
                return rational("nan")
            if oper.denominator == 1:
                return rational(self.numerator ** oper.numerator, self.denominator ** oper.numerator)
            return float(self) ** float(oper)
        if type(oper) == int:
            return rational(self.numerator ** oper, self.denominator ** oper)
        if type(oper) == float:
            return float(self) ** oper
        raise TypeError("unsupported operand type(s) for **: 'rational' and '%s'" % type(oper))

    def __rpow__(self, oper):
        if type(oper) == int:
            if self.denominator == 1:
                return rational(oper ** self.numerator)
            return oper ** float(self)
        if type(oper) == float:
            return oper ** float(self)
        raise TypeError("unsupported operand type(s) for **: 'rational' and '%s'" % type(oper))

    def __lt__(self, oper):
        if type(oper) == rational:
            if isnan(self.numerator) or isnan(oper.numerator) or isnan(self.denominator) or isnan(oper.denominator):
                return False
            if self.numerator * oper.denominator < oper.numerator * self.denominator:
                return True
            return False
        if type(oper) == int:
            if self.numerator < oper * self.denominator:
                return True
            return False
        if type(oper) == float:
            return float(self) < oper
        raise TypeError("unsupported operand type(s) for <: 'rational' and '%s'" % type(oper))

    def __le__(self, oper):
        if type(oper) == rational:
            if isnan(self.numerator) or isnan(oper.numerator) or isnan(self.denominator) or isnan(oper.denominator):
                return False
            if self.numerator * oper.denominator <= oper.numerator * self.denominator:
                return True
            return False
        if type(oper) == int:
            if self.numerator <= oper * self.denominator:
                return True
            return False
        if type(oper) == float:
            return float(self) <= oper
        raise TypeError("unsupported operand type(s) for <=: 'rational' and '%s'" % type(oper))

    def __gt__(self, oper):
        if type(oper) == rational:
            if isnan(self.numerator) or isnan(oper.numerator) or isnan(self.denominator) or isnan(oper.denominator):
                return False
            if self.numerator * oper.denominator > oper.numerator * self.denominator:
                return True
            return False
        if type(oper) == int:
            if self.numerator > oper * self.denominator:
                return True
            return False
        if type(oper) == float:
            return float(self) > oper
        raise TypeError("unsupported operand type(s) for >: 'rational' and '%s'" % type(oper))

    def __ge__(self, oper):
        if type(oper) == rational:
            if isnan(self.numerator) or isnan(oper.numerator) or isnan(self.denominator) or isnan(oper.denominator):
                return False
            if self.numerator * oper.denominator >= oper.numerator * self.denominator:
                return True
            return False
        if type(oper) == int:
            if self.numerator >= oper * self.denominator:
                return True
            return False
        if type(oper) == float:
            return float(self) > oper
        raise TypeError("unsupported operand type(s) for >=: 'rational' and '%s'" % type(oper))

    def __eq__(self, oper):
        if type(oper) == rational:
            if isnan(self.numerator) or isnan(oper.numerator) or isnan(self.denominator) or isnan(oper.denominator):
                return False
            if self.numerator * oper.denominator == oper.numerator * self.denominator:
                return True
            return False
        if type(oper) == int:
            if self.numerator == oper * self.denominator:
                return True
            return False
        if type(oper) == float:
            return float(self) == oper
        return False

    def __ne__(self, oper):
        if type(oper) == rational:
            if isnan(self.numerator) or isnan(oper.numerator) or isnan(self.denominator) or isnan(oper.denominator):
                return False
            if self.numerator * oper.denominator != oper.numerator * self.denominator:
                return True
            return False
        if type(oper) == int:
            if self.numerator != oper * self.denominator:
                return True
            return False
        if type(oper) == float:
            return float(self) != oper
        return True

    def __abs__(self):
        return rational(abs(self.numerator), self.denominator)

    def __round__(self):
        return round(float(self))

    def __bool__(self):
        if self.numerator == 0:
            return False
        return True

    def __int__(self):
        if abs(self.numerator) == float("inf"):
            raise OverflowError("cannot convert infinity to integer")
        if isnan(self.numerator) or isnan(self.denominator):
            raise ValueError("cannot convert NaN to integer")
        return int(self.numerator // self.denominator)

    def __float__(self):
        return self.numerator / self.denominator

    def normallize(self):
        if self.numerator == "inf":
            self.numerator = float("inf")
        elif self.numerator == "-inf":
            self.numerator = -float("inf")
        elif self.numerator == "nan":
            self.numerator = float("nan")
            
        if self.denominator == "inf":
            self.denominator = float("inf")
        elif self.denominator == "-inf":
            self.denominator = -float("inf")
        elif self.denominator == "nan":
            self.denominator = float("nan")

        if type(self.numerator) not in [rational, int, float] or type(self.denominator) not in [rational, int, float]:
            raise TypeError("%s cannot be numerator or denominator of 'rational' number." % type(self.numerator))

        if self.denominator == 0:
            raise ZeroDivisionError("denominator for 'rational' number can not be zero.")
        elif isnan(self.numerator) or isnan(self.denominator):
            self.numerator = self.denominator = float("nan")
            return
        elif self.numerator == 0:
            self.numerator = 0
            self.denominator = 1
            return

        if abs(self.numerator) == float("inf"):
            if abs(self.denominator) == float("inf"):
                self.numerator = self.denominator = float("nan")
                return
            else:
                self.numerator = self.numerator * self.denominator
                self.denominator = 1
                return
        elif abs(self.denominator) == float("inf"):
            self.numerator = 0
            self.denominator = 1
            return
            
        if self.denominator == 1:
            if type(self.numerator) == rational:
                self.denominator = self.numerator.denominator
                self.numerator = self.numerator.numerator
                return
            elif type(self.numerator) == int:
                return
            elif type(self.numerator) == float:
                trans = f"{self.numerator:+.15e}"
                n = (-1 if trans[0] == '-' else 1) * int(float(trans[1:18]) * 10**15)
                d = 10 ** (-int(trans[19:]) + 15)
        else:
            p = rational(self.numerator)
            q = rational(self.denominator)
            n = p.numerator * q.denominator
            d = p.denominator * q.numerator
        GCD, t = abs(n), abs(d)
        while t != 0:
            GCD, t = t, GCD%t
        self.numerator = (-1 if n * d < 0 else 1) * abs(n) // GCD
        self.denominator = abs(d) // GCD

    def reciprocal(self):
        return rational(self.denominator, self.numerator)

    def copy(self):
        return rational(self.numerator, self.denominator)
