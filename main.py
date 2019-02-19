import numpy as np
import random
import copy
import pandas as pd
from collections import OrderedDict
from functools import reduce

from src.solution import Solution
from src.funcs import create_random_solution

n_courses = 2
table_sizes = [5, 5, 5, 5]

pop_size = 100
greedy = True

random.seed(1234)

fixed = pd.read_csv('data/fixed.csv')
solutions = [Solution(create_random_solution(n_courses, table_sizes, fixed), n_courses, table_sizes, fixed) for i in
             range(pop_size)]

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

# Get the best solutions.
# Then, calculate gender disparity based on id, keep the 10 best solutions.
solutions = [{'solution': sol, 'score': sol.get_score()} for sol in solutions]
solutions = sorted(solutions, key=lambda k: k['score'])
best_solutions = [x for x in solutions if x['score']==solutions[0]['score']]
[sol.update({'gender_score': np.std([np.mean(a) for a in [y>10 for x in sol['solution'].get_plan() for y in x]])}) for sol in best_solutions]
best_solutions = sorted(best_solutions, key=lambda k: k['gender_score'])

for i in range(10):
    plan = best_solutions[i]['solution'].get_plan()
    df_plan = pd.DataFrame(OrderedDict({'course': np.concatenate([np.ones(sum(table_sizes)) * i for i in range(n_courses)]),
                                        'table': np.tile(
                                            np.concatenate([np.ones(size) * i for i, size in enumerate(table_sizes)]), 3),
                                        'person': np.concatenate([np.concatenate(x) for x in plan])}))
    names = pd.read_csv('data/names.csv')
    df_plan = df_plan.merge(names, left_on='person', right_on='id', how='left')
    df_plan['name'] = df_plan['name']
    df_plan = df_plan.drop(['id', 'code', 'person'], axis=1)
    df_plan['course'] = df_plan['course'] + 1
    df_plan['table'] = df_plan['table'] + 1

    inc_mat = best_solutions[i]['solution'].get_total_incidence_matrix()
    inc_mat = pd.DataFrame(data=inc_mat)
    inc_mat.columns = names.sort_values('id')['name'].values
    inc_mat.index = names.sort_values('id')['name'].values

    df_plan.to_csv('results/' + str(i + 1) + '_plan.csv', index=False)
    inc_mat.to_csv('results/' + str(i + 1) + '_matrix.csv')
