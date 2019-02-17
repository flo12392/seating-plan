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
solutions = [{'solution': sol, 'score': sol.get_score()} for sol in solutions]
solutions = sorted(solutions, key=lambda k: k['score'])

solution1 = solutions[10]['solution']
total_incidence_matrix = solution1.get_total_incidence_matrix()
plan = solution1.get_plan()
score = solution1.get_score()

solution2 = solution1.improve_solution(False)

