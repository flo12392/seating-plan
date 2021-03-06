from typing import List
import numpy as np
import itertools
import random
import copy


class Solution:

    def __init__(self, plan: List, n_courses: int, table_sizes: List[int]):
        self.plan = plan
        self.n_courses = n_courses
        self.table_sizes = table_sizes
        self.incidence_matrix = None
        self.score = None

        self._create_incidence_matrix()
        self._score()

    def _create_incidence_matrix(self):
        incidence_matrix = np.zeros([len(self.table_sizes), sum(self.table_sizes), sum(self.table_sizes)])
        for course in range(self.n_courses):
            for table in range(len(self.table_sizes)):
                for combination in itertools.combinations(self.plan[course][table], 2):
                    incidence_matrix[course][combination[0]][combination[1]] += 1
                    incidence_matrix[course][combination[1]][combination[0]] += 1
        self.incidence_matrix = incidence_matrix

    def _score(self):
        total_incidence_matrix = np.sum(self.incidence_matrix, axis=0)
        score = np.sum((total_incidence_matrix[total_incidence_matrix > 1]-1)**2) / 2
        if np.max(np.sum(total_incidence_matrix>1,axis=1))>0:
            stdev = np.std(np.sum(total_incidence_matrix>1,axis=1)/np.max(np.sum(total_incidence_matrix>1,axis=1)))
        else:
            stdev = 0
        self.score = np.round(score + stdev,3)

    def get_plan(self):
        return self.plan

    def get_score(self):
        return self.score

    def get_incidence_matrix(self):
        return self.incidence_matrix

    def get_total_incidence_matrix(self):
        return np.sum(self.incidence_matrix, axis=0)

    def improve_solution(self, greedy: bool, verbose = False):
        issue = random.choice(np.argwhere(self.get_total_incidence_matrix() > 1))
        conflicts = np.argwhere(
            [[all([x in self.plan[course][table] for x in issue]) for table in range(len(self.table_sizes))] for course in
             range(self.n_courses)])

        best_new_solution = None
        best_score = self.score

        for conflict in np.random.permutation(conflicts):
            course = conflict[0].item()
            table = conflict[1].item()
            for person in np.random.permutation(issue):
                index_person = np.argwhere(self.plan[course][table] == person).item()
                for other_table in np.random.permutation(list(set((range(len(self.table_sizes)))) - set([table]))):
                    for other_person in np.random.permutation(self.plan[course][other_table]):
                        index_other_person = np.argwhere(self.plan[course][other_table] == other_person).item()
                        new_plan = copy.deepcopy(self.plan)
                        new_plan[course][other_table][index_other_person] = person
                        new_plan[course][table][index_person] = other_person
                        new_solution = Solution(new_plan, self.n_courses, self.table_sizes)
                        new_score = new_solution.get_score()
                        if verbose:
                            print('conflict: ' + str(conflict) + '. Switching person ' + str(person) + ' in course ' + str(course) +
                                  ' from table ' + str(table) + ' to ' + str(other_table) + ' with person ' + str(other_person) +
                                  ' changes score from ' + str(self.score) + ' to ' + str(new_score) + '.')
                        if new_score < best_score:
                            if greedy:
                                return new_solution
                            else:
                                best_score = new_solution.get_score()
                                best_new_solution = copy.deepcopy(new_solution)

        return best_new_solution