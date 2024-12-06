from z3 import *


# In Exercise 1, we've learned how to use z3 to obtain the solutions that
# satisfy a given proposition.
# We must point out that the validity of Z3 is capable to prove
# lies into the boundary of classical logic:

# Besides "And", "Or" and "Not" constructors (functions), there
# is some also the "Implies" and "Xor" constructors, which
# can be used to construct propositions. For instance:
# P->P
P = Bool('P')
F = Implies(P, P)

# Now think of what we do in previous exercise about using `prove()`. 
# Now we use a different way, to prove it via `solve()`.
# This time we don't use z3 to obtain the solution for P->P, we just
# try to find solution for its opposite, aka. Not(F):
solve(Not(F))

# Z3 output the following:
# "no solution"
# which indicates that the proposition F is valid.

# Then the following
# double negation law:
# ~~P -> P
F = Implies(Not(Not(P)), P)
solve(Not(F))

# Exercise 2-1:
# Now it's your turn, try to prove the exclusive middle law if also valid:
# P \/ ~P
print("Exercise 2-1:")
P = Bool('P')
F = Or(P, Not(P))
solve(Not(F))

# Exercise 2-2:
# Prove the validity of the Pierce's law:
# ((P->Q)->P)->P)
print("Exercise 2-2:")
P, Q = Bools('P Q')
F = Implies(Implies(Implies(P, Q), P), P)
solve(Not(F))

# Note that the Pierce's law only holds in classical logic, but
# not in constructive logic, for
# interested readers, please refer to the background reading:
# https://en.wikipedia.org/wiki/Peirce%27s_law

# Exercise 2-3:
# In previous exercise about use Coq, we ever give you an challenge
# (P -> Q) -> (~Q -> ~P).
# Now try to prove it's valid via z3
print("Exercise 2-3:")
P, Q = Bools('P Q')
F = Implies(Implies(P, Q), Implies(Not(Q), Not(P)))
solve(Not(F))

# Exercise 2-4:
# Once more, try to prove that validity of :
# (P -> Q /\ R) -> ((P -> Q) /\ (P -> R))
# Be carefully when you process the priority of operations cause
# there is no intros. which can process it automatically for you
# to use.
print("Exercise 2-4:")
P, Q, R = Bools('P Q R')
F = Implies(Implies(P, And(Q, R)), And(Implies(P, Q), Implies(P, R)))
solve(Not(F))

# Well done, you complete Exercise 2, remember to save your src for handing in.
