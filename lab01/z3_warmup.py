import z3

# Find solution set that can make logical expression P/\Q be true

# Define proposition P and Q
P, Q = z3.Bools('P Q')

# Define proposition F = P/\Q
F = z3.And(P, Q)
F_test = z3.Not(Q)

# Create solver
solver = z3.Solver()

# Add the proposition to the solver
solver.add(F)
solver.add(F_test)

# Check if the solver is solvable
print(solver.check())

# Print the solver's result
if solver.check() == z3.sat:
    print(solver.model())

z3.prove(F)

z3.prove(F_test)
