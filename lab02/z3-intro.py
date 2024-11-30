from z3 import *
from pro_print import *

# Z3 is an SMT solver. In this lecture, we'll discuss
# the basis usage of Z3 through some working example, the
# primary goal is to introduce how to use Z3 to solve
# the satisfiability problems we've discussed in the past
# several lectures.
# We must emphasize that Z3 is just one of the many such SMT
# solvers, and by introducing Z3, we hope you will have a
# general understanding of what such solvers look like, and
# what they can do.

########################################
# Basic propositional logic

# In Z3, we can declare two propositions just as booleans, this
# is rather natural, for propositions can have values true or false.
# To declare two propositions P and Q:
P = Bool("P")
Q = Bool("Q")
# or, we can use a more compact shorthand:
P, Q = Bools("P Q")


# We can build propositions by writing Lisp-style abstract
# syntax trees, for example, the disjunction:
# P \/ Q
# can be encoded as the following AST:
F = Or(P, Q)
# Output is : Or(P, Q)
print(F)

# Note that the connective '\/' is called 'Or' in Z3, we'll see
# several other in the next.

# We have designed the function 'pretty_print(expr)' for you,
# As long as we input the expression defined by z3, we can output
# propositions that are suitable for us to read.
# Here‘s an example:

P, Q = Bools("P Q")
F = Or(P, Q)

# Output is : P \/ Q
pretty_print(F)

print("################################################################")
print("##                           Part A                           ##")
print("################################################################")

################################################################
##                           Part A                           ##
################################################################

# exercises 1 : P -> (Q -> P)
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
print(f"{'#' * 15} exercise 1 {'#' * 15}")
P, Q = Bools("P Q")
F = Implies(P, Implies(Q, P))
z3.prove(F)
pretty_print(F)

# exercise 2 : (P -> Q) -> ((Q -> R) -> (P -> R))
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
print(f"{'#' * 15} exercise 2 {'#' * 15}")
P, Q, R = Bools("P Q R")
F = Implies(Implies(P, Q), Implies(Implies(Q, R), Implies(P, R)))
z3.prove(F)
pretty_print(F)

# exercise 3 : (P /\ (Q /\ R)) -> ((P /\ Q) /\ R)
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
print(f"{'#' * 15} exercise 3 {'#' * 15}")
P, Q, R = Bools("P Q R")
F = Implies(And(P, And(Q, R)), And(And(P, Q), R))
z3.prove(F)
pretty_print(F)

# exercise 4 : (P \/ (Q \/ R)) -> ((P \/ Q) \/ R)
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
print(f"{'#' * 15} exercise 4 {'#' * 15}")
P, Q, R = Bools("P Q R")
F = Implies(Or(P, Or(Q, R)), Or(Or(P, Q), R))
z3.prove(F)
pretty_print(F)

# exercise 5 : ((P -> R) /\ (Q -> R)) -> ((P /\ Q) -> R)
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
print(f"{'#' * 15} exercise 5 {'#' * 15}")
P, Q, R = Bools("P Q R")
F = Implies(And(Implies(P, R), Implies(Q, R)), Implies(And(P, Q), R))
z3.prove(F)
pretty_print(F)

# exercise 6 : ((P /\ Q) -> R) <-> (P -> (Q -> R))
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
print(f"{'#' * 15} exercise 6 {'#' * 15}")
P, Q, R = Bools("P Q R")
F1 = Implies(And(P, Q), R)
F2 = Implies(P, Implies(Q, R))
F = And(Implies(F1, F2), Implies(F2, F1))
z3.prove(F)
pretty_print(F)

# exercise 7 : (P -> Q) -> (¬Q -> ¬P)
# Please use z3 to define the proposition
# Note that you need to define the proposition, and prove it.
print(f"{'#' * 15} exercise 7 {'#' * 15}")
P, Q = Bools("P Q")
F = Implies(Implies(P, Q), Implies(Not(Q), Not(P)))
z3.prove(F)
pretty_print(F)

print("################################################################")
print("##                           Part B                           ##")
print("################################################################")
################################################################
##                           Part B                           ##
################################################################

# Before writing the src first, we need to understand the
# quantifier. ∀ x.P (x) means that for any x, P (x) holds,
# so both x and P should be a sort types. IntSort() and BoolSort()
# are given in Z3
# IntSort(): Return the integer sort in the given context.
# BoolSort(): Return the Boolean Z3 sort.
isort = IntSort()
bsort = BoolSort()

# Declare a Int variable x
x = Int("x")

# Declare a function P with input of isort type and output
# of bsort type
P = Function("P", isort, bsort)

# It means ∃x.P(x)
F = Exists(x, P(x))
print(F)
pretty_print(F)

# Now you can complete the following exercise based on the example above

# exercise 8 : # ∀x.(¬P(x) /\ Q(x)) -> ∀x.(P(x) -> Q(x))
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
print(f"{'#' * 15} exercise 8 {'#' * 15}")
P = Function("P", isort, bsort)
Q = Function("Q", isort, bsort)
F = Implies(ForAll(x, And(Not(P(x)), Q(x))), ForAll(x, Implies(P(x), Q(x))))
z3.prove(F)
pretty_print(F)

# exercise 9 : ∀x.(P(x) /\ Q(x)) <-> (∀x.P(x) /\ ∀x.Q(x))
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
print(f"{'#' * 15} exercise 9 {'#' * 15}")
P = Function("P", isort, bsort)
Q = Function("Q", isort, bsort)
F1 = ForAll(x, And(P(x), Q(x)))
F2 = And(ForAll(x, P(x)), ForAll(x, Q(x)))
F = And(Implies(F1, F2), Implies(F2, F1))
z3.prove(F)
pretty_print(F)

# exercise 10 : ∃x.(¬P(x) \/ Q(x)) -> ∃x.(¬(P(x) /\ ¬Q(x)))
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
print(f"{'#' * 15} exercise 10 {'#' * 15}")
P = Function("P", isort, bsort)
Q = Function("Q", isort, bsort)
F = Implies(Exists(x, Or(Not(P(x)), Q(x))), Exists(x, Not(And(P(x), Not(Q(x))))))
z3.prove(F)
pretty_print(F)

# exercise 11 : ∃x.(P(x) \/ Q(x)) <-> (∃x.P(x) \/ ∃x.Q(x))
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
print(f"{'#' * 15} exercise 11 {'#' * 15}")
P = Function("P", isort, bsort)
Q = Function("Q", isort, bsort)
F1 = Exists(x, Or(P(x), Q(x)))
F2 = Or(Exists(x, P(x)), Exists(x, Q(x)))
F = And(Implies(F1, F2), Implies(F2, F1))
z3.prove(F)
pretty_print(F)

# exercise 12 : ∀x.(P(x) -> ¬Q(x)) -> ¬(∃x.(P(x) /\ Q(x)))
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
print(f"{'#' * 15} exercise 12 {'#' * 15}")
P = Function("P", isort, bsort)
Q = Function("Q", isort, bsort)
F = Implies(ForAll(x, Implies(P(x), Not(Q(x)))), Not(Exists(x, And(P(x), Q(x)))))
z3.prove(F)
pretty_print(F)

# exercise 13 : ∃x.(P(x) /\ Q(x)) /\ ∀x.(P(x) -> R(x)) -> ∃x.(R(x) /\ Q(x))
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
print(f"{'#' * 15} exercise 13 {'#' * 15}")
P = Function("P", isort, bsort)
Q = Function("Q", isort, bsort)
R = Function("R", isort, bsort)
F = Implies(And(Exists(x, And(P(x), Q(x))), ForAll(x, Implies(P(x), R(x)))), Exists(x, And(R(x), Q(x))))
z3.prove(F)
pretty_print(F)

# exercise 14 : ∃x.∃y.P(x, y) -> ∃y.∃x.P(x, y)
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
print(f"{'#' * 15} exercise 14 {'#' * 15}")
P = Function("P", isort, isort, bsort)
y = Int("y")
F = Implies(Exists(x, Exists(y, P(x, y))), Exists(y, Exists(x, P(x, y))))
z3.prove(F)
pretty_print(F)

# exercise 15 : P(b) /\ (∀x.∀y.(P(x) /\ P(y) -> x = y)) -> (∀x.(P(x) <-> x = b))
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
print(f"{'#' * 15} exercise 15 {'#' * 15}")
P = Function("P", isort, bsort)
b = Int("b")
y = Int("y")
F1 = And(P(b), ForAll([x, y], Implies(And(P(x), P(y)), x == y)))
F2 = P(x)
F3 = x == b
F = Implies(F1, ForAll(x, And(Implies(F2, F3), Implies(F3, F2))))
z3.prove(F)
pretty_print(F)

print("################################################################")
print("##                           Part C                           ##")
print("################################################################")
################################################################
##                           Part C                           ##
################################################################

# Challenge:
# We provide the following two rules :
#     ----------------(odd_1)
#           odd 1
#
#           odd n
#     ----------------(odd_ss)
#         odd n + 2
#
# Please prove that integers 9, 25, and 99 are odd numbers.

# declare sorts: isort and bsort
isort = IntSort()
bsort = BoolSort()

# Create a function 'odd' that takes an integer and returns a boolean
odd = Function('odd', isort, bsort)

# Create solver
s = Solver()

# Add the rules as axioms
# Rule odd_1: odd(1) is true
s.add(odd(1))

# Rule odd_ss: For any n, if odd(n) then odd(n+2)
n = Int('n')
s.add(ForAll([n], Implies(odd(n), odd(n + 2))))

# Numbers to prove are odd
numbers_to_prove = [9, 25, 99]

# Create separate proofs for each number
for num in numbers_to_prove:
    print(f"\nTrying to prove {num} is odd...")
    s.push()
    s.add(Not(odd(num)))  # Try to prove by contradiction
    
    if s.check() == unsat:
        print(f"{num} is proven to be odd")
    else:
        print(f"Could not prove {num} is odd")
    
    s.pop()
