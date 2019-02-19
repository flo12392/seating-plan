import numpy as np
import random
import copy

from src.solution import Solution

n_courses = 3
table_sizes = [8,7,7]

pop_size = 2500
greedy = True

random.seed(1234)

solutions = [Solution([np.split(np.random.permutation(np.arange(sum(table_sizes))), np.cumsum(table_sizes)[:-1]) for x in
                       range(n_courses)], n_courses, table_sizes) for y in range(pop_size)]

for i, solution in enumerate(solutions):
    if i % 100 == 0:
        print(str(i) + '/' + str(pop_size))
    local_optimum = (solution.get_score() == 0)
    while not local_optimum:
        new_solution = solution.improve_solution(greedy)
        if new_solution is None:
            local_optimum = True
        else:
            solution = new_solution
            if new_solution.get_score() == 0:
                local_optimum = True

    solutions[i] = solution

solutions = [{'solution': sol, 'score': sol.get_score()} for sol in solutions]
solutions = sorted(solutions, key=lambda k: k['score'])


