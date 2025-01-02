from dataclasses import dataclass
import unittest

from z3 import *

# uninterrupted functions
S = Function("S", IntSort(), IntSort())
H = Function("H", IntSort(), IntSort())


# syntax of pointers
#
# T ::= x | T + E | &x | &*T | *T | NULL
# E ::= x | n | E + E | E - E | *T
# R ::= T = T | T < T | E = E | E < E
# P ::= R | ~R | P ∧ P
#
#
# Term based
@dataclass(repr=False)
class Term:
    def __repr__(self):
        return self.__str__()
    
    
# Expression based
@dataclass(repr=False)
class Expr:
    def __repr__(self):
        return self.__str__()


# Terms
@dataclass(repr=False)
class TVar(Term):
    name: str

    def __str__(self):
        return self.name


@dataclass(repr=False)
class TAddE(Term):
    term: Term
    expr: Expr

    def __str__(self):
        return f"{self.term} + {self.expr}"


@dataclass(repr=False)
class TAddr(Term):
    var: TVar 

    def __str__(self):
        return f"&{self.var.name}"


@dataclass(repr=False)
class TAddrStar(Term):
    term: Term

    def __str__(self):
        if isinstance(self.term, TAddE):
            return f"&*({self.term})"
        return f"&*{self.term}"


@dataclass(repr=False)
class TStar(Term):
    term: Term

    def __str__(self):
        if isinstance(self.term, TAddE):
            return f"*({self.term})"
        return f"*{self.term}"

@dataclass(repr=False)
class TNull(Term):
    def __str__(self):
        return "NULL"
    

# Expressions
@dataclass(repr=False)
class EVar(Expr):
    name: str

    def __str__(self):
        return self.name


@dataclass(repr=False)
class EConst(Expr):
    value: int | float

    def __str__(self):
        return f"{self.value}"


@dataclass(repr=False)
class EAdd(Expr):
    left: Expr
    right: Expr

    def __str__(self):
        return f"({self.left} + {self.right})"


@dataclass(repr=False)
class EMinus(Expr):
    left: Expr
    right: Expr

    def __str__(self):
        return f"({self.left} - {self.right})"


@dataclass(repr=False)
class EStar(Expr):
    term: Term

    def __str__(self):
        return f"*{self.term}"


# Relations
@dataclass(repr=False)
class Relation:
    def __repr__(self):
        return self.__str__()


@dataclass(repr=False)
class RTEq(Relation):
    left: Term
    right: Term

    def __str__(self):
        return f"({self.left} = {self.right})"


@dataclass(repr=False)
class RTLe(Relation):
    left: Term
    right: Term

    def __str__(self):
        return f"({self.left} < {self.right})"


@dataclass(repr=False)
class REEq(Relation):
    left: Expr
    right: Expr

    def __str__(self):
        return f"({self.left} = {self.right})"


@dataclass(repr=False)
class RELe(Relation):
    left: Expr
    right: Expr

    def __str__(self):
        return f"({self.left} < {self.right})"


# Formula
@dataclass(repr=False)
class Prop:
    def __repr__(self):
        return self.__str__()


@dataclass(repr=False)
class PRel(Prop):
    rel: Relation

    def __str__(self):
        return f"{self.rel}"


@dataclass(repr=False)
class PNot(Prop):
    rel: Relation

    def __str__(self):
        return f"~{self.rel}"


@dataclass(repr=False)
class PAnd(Prop):
    left: Prop
    right: Prop

    def __str__(self):
        return f"({self.left} /\\ {self.right})"


def count_stars(prop: Prop):
    # @Exercise 17: finish the missing src in `count_stars()` methods,
    # make it can count amount of star symbols (*) in our pointer logic.
    
    def term_count_stars(term: Term):
        # your src here
        raise NotImplementedError('TODO: Your code here!') 

    def expr_count_stars(expr: Expr):
        # your src here
        raise NotImplementedError('TODO: Your code here!') 

    def rel_count_stars(rel: Relation):
        # your src here
        raise NotImplementedError('TODO: Your code here!') 

    match prop:
        case PRel(rel) | PNot(rel):
            return rel_count_stars(rel)
        case PAnd(left, right):
            return count_stars(left) + count_stars(right)


def to_z3(prop: Prop):
    # @Exercise 18: finish the missing src in `to_z3()` methods,
    # make it can translates pointer logic to z3's constraints.

    def term_to_z3(term: Term):
        # rules to eliminate a pointer T
        #
        # ⟦x⟧      =   H(S(x))
        # ⟦T + E⟧  =   ⟦T⟧ + ⟦E⟧
        # ⟦&x⟧     =   S(x)
        # ⟦&*T⟧    =   ⟦T⟧
        # ⟦*T⟧     =   H(⟦T⟧)
        # ⟦NULL⟧   =   0
        #
        # your src here
        raise NotImplementedError('TODO: Your code here!') 

    def expr_to_z3(expr: Expr):
        # rules to eliminate an expression E
        #
        # ⟦n⟧      =   n
        # ⟦x⟧      =   H(S(x))
        # ⟦E + E⟧  =   ⟦E⟧ + ⟦E⟧
        # ⟦E − E⟧  =   ⟦E⟧ − ⟦E⟧
        # ⟦*T⟧     =   H(⟦T⟧)
        #
        # your src here
        raise NotImplementedError('TODO: Your code here!') 

    def relation_to_z3(rel: Relation):
        # rules to eliminate a relation R
        #
        # ⟦T = T⟧   =   ⟦T⟧ = ⟦T⟧
        # ⟦T < T⟧   =   ⟦T⟧ < ⟦T⟧
        # ⟦E = E⟧   =   ⟦E⟧ = ⟦E⟧
        # ⟦E < E⟧   =   ⟦E⟧ < ⟦E⟧
        #
        # your src here
        raise NotImplementedError('TODO: Your code here!') 

    # rules to eliminate a proposition P
    #
    # ⟦R⟧      =   ⟦R⟧
    # ⟦~R⟧     =   ~⟦R⟧
    # ⟦P /\Q⟧  =   ⟦P⟧ / \ ⟦Q⟧
    #
    match prop:
        case PRel(rel):
            return relation_to_z3(rel)
        case PNot(rel):
            return Not(relation_to_z3(rel))
        case PAnd(left, right):
            return And(to_z3(left), to_z3(right))


######################
# unit test
p1 = PAnd(PRel(RTEq(TVar("p"),
                    TAddr(TVar("q")))
               ),
          PRel(REEq(EVar("q"),
                    EConst(1))
               )
          )

p2 = PRel(REEq(EStar(TVar("p")), EConst(1)))


p3 = PAnd(PRel(RTEq(TStar(TAddrStar(TVar("p"))),
                    TAddrStar(TStar(TVar("q"))))
               ),
          PRel(REEq(EStar(TStar(TStar(TVar("p")))),
                    EStar(TAddrStar(TAddE(TStar(TVar("q")), EConst(1)))))
               )
          )

# ((p = &q) /\ (q = 1)) -> (*p = 1)
print(f"{p1} -> {p2}")

# ((*&*p = &**q) /\ (***p = *&**q + (1)))
print(p3)


class TestPointer(unittest.TestCase):
    def test_count_starts(self):
        self.assertEqual((count_stars(p1)), 0)
        self.assertEqual((count_stars(p2)), 1)
        self.assertEqual((count_stars(p3)), 10)

    def test_to_z3(self):
        p = Implies(to_z3(p1), to_z3(p2))
        self.assertEqual(str(p), "Implies(And(H(S(p)) == S(q), H(S(q)) == 1), H(H(S(p))) == 1)")

        solver = Solver()
        solver.add(Not(p))
        self.assertEqual(solver.check(), unsat)
    

if __name__ == '__main__':
    unittest.main()
