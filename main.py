import numpy as np
import random
import copy

from src.solution import Solution

n_persons = 9
n_tables = 3
n_courses = 3
table_sizes = [3, 3, 3]

pop_size = 100
greedy = False

random.seed(1234)

if sum(table_sizes) != n_persons:
    raise ValueError('The number of persons does not match the number of seats at the tables')

persons = np.arange(n_persons)

solutions = [Solution([np.split(np.random.permutation(np.copy(persons)), np.cumsum(table_sizes)[:-1]) for x in
                       range(n_courses)], n_persons, n_tables, n_courses) for y in range(pop_size)]

for i, solution in enumerate(solutions):
    print(' ---- NEW SOLUTION ----')
    print(str(solution.get_score()))

    local_optimum = (solution.get_score() == 0)

    while not local_optimum:
        new_solution = solution.improve_solution(greedy)
        if new_solution is None or new_solution.get_score() == 0:
            print('Local optimum found.')
            local_optimum = True
        else:
            solution = new_solution
            print(str(solution.get_score()))

    solutions[i] = solution
