import unittest
from typing import List
from dataclasses import dataclass

from z3 import *

# In this problem, you will implement the DPLL algorithm as discussed
# in the class.

########################################
# This bunch of src declare the syntax for the propositional logic, we
# repeat here:
'''
P ::= p
    | T
    | F
    | P /\ P
    | P \/ P
    | P -> P
    | ~P
'''

@dataclass
class Prop:
    def __repr__(self):
        return self.__str__()
        


@dataclass(repr=False)
class PVar(Prop):
    var: str

    def __str__(self):
        return self.var
    
    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.var)


@dataclass(repr=False)
class PTrue(Prop):
    def __str__(self):
        return "True"


@dataclass(repr=False)
class PFalse(Prop):
    def __str__(self):
        return "False"
    

@dataclass(repr=False)
class PAnd(Prop):
    left: Prop
    right: Prop

    def __str__(self):
        return f"({self.left} /\\ {self.right})"


@dataclass(repr=False)
class POr(Prop):
    left: Prop
    right: Prop

    def __str__(self):
        return f"({self.left} \\/ {self.right})"


@dataclass(repr=False)
class PImplies(Prop):
    left: Prop
    right: Prop

    def __str__(self):
        return f"({self.left} -> {self.right})"


@dataclass(repr=False)
class PNot(Prop):
    p: Prop

    def __str__(self):
        return f"~{self.p}"


# Exercise 3-1: try to complete the `to_z3()` method to make
# we can convert the above defined syntax into Z3's representation, so
# that we can check it's validity easily:
def to_z3(prop: Prop) -> z3.BoolRef:
    match prop:
        case PVar(var):
            return Bool(var)
        case PTrue():
            return True
        case PFalse():
            return False
        case PAnd(left, right):
            return And(to_z3(left), to_z3(right))
        case POr(left, right):
            return Or(to_z3(left), to_z3(right))
        case PImplies(left, right):
            return Implies(to_z3(left), to_z3(right))
        case PNot(p):
            return Not(to_z3(p))



#####################
# Exercise 3-2: try to implement the `ie()` method to do the 
# implication elimination, as we've discussed in the class.
# recall the conversion rules:
#   C(p)      = p
#   C(~P)     = ~C(P)
#   C(P/\Q)   = C(P) /\ C(Q)
#   C(P\/Q)   = C(P) \/ C(Q)
#   C(P->Q)   = ~C(P) \/ C(Q)

def ie(prop: Prop) -> Prop:
    match prop:
        case PVar(var):
            return prop
        case PTrue():
            return prop
        case PFalse():
            return prop
        case PAnd(left, right):
            return PAnd(ie(left), ie(right))
        case POr(left, right):
            return POr(ie(left), ie(right))
        case PImplies(left, right):
            return POr(PNot(ie(left)), ie(right))
        case PNot(p):
            return PNot(ie(p))
        # raise NotImplementedError('TODO: Your code here!') 


# Exercise 3-3: try to implement the `nnf()` method to convert the
# proposition to nnf, as we've discussed in the class.
# recall the conversion rules:
#   C(p)       = p
#   C(~p)      = ~p
#   C(~~P)     = C(P)
#   C(P/\Q)    = C(P) /\ C(Q)
#   C(P\/Q)    = C(P) \/ C(Q)
#   C(~(P/\Q)) = C(~P) \/ C(~Q)
#   C(~(P\/Q)) = C(~P) /\ C(~Q)
def nnf(prop_without_implies: Prop) -> Prop:
    match prop_without_implies:
        case PVar(var):
            return prop_without_implies
        case PTrue():
            return prop_without_implies
        case PFalse():
            return prop_without_implies
        case PAnd(left, right):
            return PAnd(nnf(left), nnf(right))
        case POr(left, right):
            return POr(nnf(left), nnf(right))
        case PNot(PNot(p)):
            return nnf(p)
        case PNot(PAnd(left, right)):
            return POr(nnf(PNot(left)), nnf(PNot(right)))
        case PNot(POr(left, right)):
            return PAnd(nnf(PNot(left)), nnf(PNot(right)))
        case PNot(p):
            return PNot(nnf(p))
        # raise NotImplementedError('TODO: Your code here!')


# Exercise 3-4: try to implement the `cnf()` method to convert the
# proposition to cnf, as we've discussed in the class.
# recall the conversion rules:
#   C(p)    = p
#   C(~p)   = ~p
#   C(P/\Q) = C(P) /\ C(Q)
#   C(P\/Q) = D(C(P), C(Q))
#
#   D(P=P1/\P2, Q) = D(P1, Q) /\ D(P2, Q)
#   D(P, Q=Q1/\Q2) = D(P, Q1) /\ D(P, Q2)
#   D(P, Q)        = P \/ Q
def cnf(nnf_prop: Prop) -> Prop:
    def cnf_d(left: Prop, right: Prop) -> Prop:
        match (left, right):
            case (PAnd(l1, l2), _):
                return PAnd(cnf_d(l1, right), cnf_d(l2, right))
            case (_, PAnd(r1, r2)):
                return PAnd(cnf_d(left, r1), cnf_d(left, r2))
            case _:
                return POr(left, right)
                
    match nnf_prop:
        case PAnd(left, right):
            return PAnd(cnf(left), cnf(right))
        case POr(left, right):
            return cnf_d(cnf(left), cnf(right))
        case _:
            return nnf_prop

def flatten(cnf_prop: Prop) -> List[List[Prop]]:
    """Flatten CNF Propositions to nested list structure .

    The CNF Propositions generated by `cnf` method is AST.
    This method can flatten the AST to a nested list of Props.
    For example: "((~p1 \\/ ~p3) /\\ (~p1 \\/ p4))" can be
    transfer to "[[~p1, ~p3], [~p1, p4]]".

    Parameters
    ----------
    cnf_prop : Prop
        CNF Propositions generated by `cnf` method.

    Returns
    -------
    List[List[Prop]
        A nested list of Props, first level lists are connected by `And`,
        and second level lists is connected by `Or`.

    """
    
    def get_atom_from_disjunction(prop: Prop) -> List[Prop]:
        match prop:
            case POr(left, right):
                return get_atom_from_disjunction(left) + get_atom_from_disjunction(right)
            case _:
                return [prop]
    
    match cnf_prop:
        case PAnd(left, right):
            return flatten(left) + flatten(right)
        case POr():
            return [get_atom_from_disjunction(cnf_prop)]
        case _ :
            return [[cnf_prop]]


def dpll(prop: Prop) -> dict:
    cnf_flat = flatten(cnf(nnf(ie(prop))))
    print(cnf_flat)
    
    # Challenge: implement the dpll algorithm we've discussed in the lecture
    # you can deal with flattened cnf which generated by `flatten` method for convenience,
    # or, as another choice, you can process the original cnf destructure generated by `cnf` method
    #
    # your implementation should output the result as dict like :
    # {"p1": True, "p2": False, "p3": False, "p4": True} if there is solution;
    # output "unsat" if there is no solution
    #
    # feel free to add new method.
    raise NotImplementedError('TODO: Your code here!') 


#####################
# test cases:

# p -> (q -> ~p)
test_prop_1 = PImplies(PVar('p'), PImplies(PVar('q'), PVar('p')))

# ~((p1 \/ ~p2) /\ (p3 \/ ~p4))
test_prop_2 = PNot(PAnd(
    POr(PVar("p1"), PNot(PVar("p2"))),
    POr(PVar("p3"), PNot(PVar("p4")))
))


# #####################
class TestDpll(unittest.TestCase):
    def test_to_z3_1(self):
        self.assertEqual(str(to_z3(test_prop_1)), "Implies(p, Implies(q, p))")

    def test_to_z3_2(self):
        self.assertEqual(str(to_z3(test_prop_2)), "Not(And(Or(p1, Not(p2)), Or(p3, Not(p4))))")

    def test_ie_1(self):
        self.assertEqual(str(ie(test_prop_1)), "(~p \\/ (~q \\/ p))")
    
    def test_ie_2(self):
        self.assertEqual(str(ie(test_prop_2)), "~((p1 \\/ ~p2) /\\ (p3 \\/ ~p4))")
    
    def test_nnf_1(self):
        self.assertEqual(str(nnf(ie(test_prop_1))), "(~p \\/ (~q \\/ p))")

    def test_nnf_2(self):
        self.assertEqual(str(nnf(ie(test_prop_2))), "((~p1 /\\ p2) \\/ (~p3 /\\ p4))")

    def test_cnf_1(self):
        self.assertEqual(str(cnf(nnf(ie(test_prop_1)))), "(~p \\/ (~q \\/ p))")

    def test_cnf_2(self):
        self.assertEqual(str(cnf(nnf(ie(test_prop_2)))),
                         "(((~p1 \\/ ~p3) /\\ (~p1 \\/ p4)) /\\ ((p2 \\/ ~p3) /\\ (p2 \\/ p4)))")

    def test_cnf_flatten_1(self):
        test_1_flatten = flatten(cnf(nnf(ie(test_prop_1))))
        self.assertEqual(str(test_1_flatten), "[[~p, ~q, p]]")

    def test_cnf_flatten_2(self):
        test_2_flatten = flatten(cnf(nnf(ie(test_prop_2))))
        self.assertEqual(str(test_2_flatten), "[[~p1, ~p3], [~p1, p4], [p2, ~p3], [p2, p4]]")

    def test_dpll_1(self):
        s = Solver()
        res = dpll(test_prop_1)
        s.add(Not(Implies(res["p"], Implies(res["q"], res["p"]))))
        self.assertEqual(str(s.check()), "unsat")

    def test_dpll_2(self):
        s = Solver()
        res = dpll(test_prop_2)
        s.add(Not(Not(And(Or(res["p1"], Not(res["p2"])), Or(res["p3"], Not(res["p4"]))))))
        self.assertEqual(str(s.check()), "unsat")


if __name__ == '__main__':
    unittest.main()
