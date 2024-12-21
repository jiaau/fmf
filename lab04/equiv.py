from z3 import *


# program equivalence:
# in the class, we present two implementation of the same algorithms, one
# is:
'''
int power3(int in){
  int i, out_a;
  out_a = in;
  for(i = 0; i < 2; i++)
    out_a = out_a * in;
  return out_a;
}
'''
# and the other one is:
'''
int power3_new(int in){
  int out_b;
  out_b = (in*in)*in;
  return out_b;
}

'''
# and with EUF, we can prove that these two algorithms are equivalent,
# that is:
# P1/\P2 -> out_a==out_b

# Exercise 2: try to prove the algorithm 'power3' and 'power3_new' 
# are equivalent by using EUF theory
# Please construct, manually, the propositions P1 and P2, and let Z3
# prove the above implication. (Note that you don't need to generate
# P1 or P2 automatically, just write down them manually.)
# raise NotImplementedError('TODO: Your code here!') 


# Define the power3 program
in_var = Int('in')
i = Int('i')
out_a = Int('out_a')
P1 = And(out_a == in_var, out_a == out_a * in_var, out_a == out_a * in_var)

# Define the power3_new program
in_var = Int('in')
out_b = Int('out_b')
P2 = out_b == (in_var * in_var) * in_var

# Define the equivalence
equiv = Implies(And(P1, P2), out_a == out_b)

# Create a solver and add the equivalence
solver = Solver()
solver.add(Not(equiv))

# Check if the equivalence holds
if solver.check() == unsat:
  print("The programs are equivalent")
else:
  print("The programs are not equivalent")