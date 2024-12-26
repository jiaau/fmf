
class AddMissingCode(BaseException):
    pass
def TODO():
    raise AddMissingCode()




""" The subset problem

The subset problem is a well-known satisfiability problem: given
a multiset (a multiset is like a normal set, expect for the
elements can be duplicated) S, whether or not there is a
non-empty subset T of S, such that:
  \\sum T = 0

For example, given this set
  {-7, -3, -2, 9000, 5, 8}
the answer is yes because the subset
  {-3, -2, 5}
sums to zero.

This problem is NPC, and for more background information of the
subset problem, please refer to:
https://en.wikipedia.org/wiki/Subset_sum_problem

"""
from typing import List, Tuple

from z3 import *
import time


# LA-based solution
def subset_sum_la(target_set: List[int]) -> Tuple[bool, List[int]]:
    solver = Solver()
    flags = [Int(f"x_{i}") for i in range(len(target_set))]

    # 0-1 ILA
    for flag in flags:
        solver.add(Or(flag == 0, flag == 1))

    # the selected set must be non-empty
    solver.add(sum(flags) != 0)

    # @Exercise 9: please fill in the missing code to add
    # the following constraint into the solver.
    #       \sum_i flags[i]*target_set[i] = 0
    # Please add your code here:
    cons_exp = []
    for i in range(len(target_set)):
        cons_exp.append(flags[i] * target_set[i])
    solver.add(sum(cons_exp) == 0)


    start = time.time()
    result = solver.check()
    end = time.time()
    print(f"time used in LA: {(end - start):.6f}s")

    if result == sat:
        return True, [target_set[index] for index, flag in enumerate(flags) if solver.model()[flag] == 1]
    return False, result


# dynamic programming-based (DP) solution (do not confuse DP with LP):
def subset_sum_dp(target_set: List[int]) -> bool:
    def doit(the_set: List[int], target: int, index: int) -> bool:
        if index == 0:
            return False
        if target == the_set[index - 1]:
            return True
        if doit(the_set, target, index - 1):
            return True
        return doit(the_set, target - the_set[index - 1], index - 1)

    start = time.time()
    result = doit(target_set, 0, len(target_set))
    end = time.time()
    print(f"time used in DP: {(end - start):.6f}s")
    return result


# to generate a list of "n" elements with the
# last two elements being "1" and "-1".
# i.e., this function returns [10000, 10000, ..., 10000, 1, -1].
def gen_large_test(n: int) -> List[int]:
    nums = [10000] * n
    nums[len(nums) - 2] = 1
    nums[len(nums) - 1] = -1
    # print(nums)
    return nums


if __name__ == '__main__':
    # a small test case
    small_set = [-7, -3, -2, 9000, 5, 8]
    subset_sum_dp(small_set)
    print(subset_sum_la(small_set))

    # a large test case
    max_nums = 20
    large_set = gen_large_test(max_nums)

    # @Exercise 10: compare the efficiency of the DP and the
    # LP algorithm, by changing the value of "max_nums" to other
    # values, say, 200, 2000, 20000, 200000, ...
    # what's your observation? What conclusion you can draw from these data?
    # Please add your code here:
    print("max_nums = 20")
    subset_sum_dp(large_set)
    print(subset_sum_la(large_set))
    print("max_nums = 200")
    max_nums = 200
    large_set = gen_large_test(max_nums)
    # subset_sum_dp(large_set)
    print(subset_sum_la(large_set))

'''
time used in DP: 0.000005s
time used in LA: 0.003499s
(True, [-3, -2, 5])
max_nums = 20
time used in DP: 0.040007s
time used in LA: 0.012928s
(True, [1, -1])
max_nums = 200
time used in LA: 0.072360s
(True, [1, -1])
'''

# when max_nums = 6, the DP algorithm is faster than the LA algorithm.
# however, when max_nums becomes larger, the LA algorithm is faster than the DP algorithm.
# the DP algorithm cannot handle large numbers of elements in the list, while the LA algorithm can handle large numbers of elements in the list. 