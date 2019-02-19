import numpy as np
import random

def create_random_solution(n_courses, table_sizes, fixed):
    plan = [[[] for x in range(len(table_sizes))] for x in range(n_courses)]
    for course in range(n_courses):
        this_course_random = set(range(sum(table_sizes))) - set(fixed['id'][(fixed['course'] == course)])
        for table in range(len(table_sizes)):
            this_fixed = list(fixed['id'][(fixed['course'] == course) & (fixed['table'] == table)])
            if len(this_fixed) > 0:
                plan[course][table].extend(this_fixed)
            random_sample = random.sample(this_course_random, table_sizes[table] - len(this_fixed))
            plan[course][table].extend(random_sample)
            this_course_random = this_course_random - set(random_sample)

    return [[np.asarray(plan[i][j]) for j in range(len(table_sizes))] for i in range(n_courses)]
