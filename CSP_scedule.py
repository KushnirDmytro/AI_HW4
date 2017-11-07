import copy


class CSP(object):
    def __init__(self):
        self.variables = []
        self.domains = {}
        #self.factors = {}
        self.domains_pack = {}
        self.assigned_domains = {}

    def add_variable(self, variable, domain):
        """
        Takes variable and its domain and adds them to the CSP
        :param variable: any type
        :param domain: list of possible values for teh variable
        """
        if variable in self.variables: raise ValueError('This CSP already contains variable', variable,
                                                        ', please use another name or check the consistency of your code.')
        if type(domain) is not list: raise ValueError('Domain should be a list.')
        self.variables.append(variable)
        self.domains[variable] = domain

    def add_factor(self, variables, factor_function):
        """
        Takes variables and the potential for these variables and adds them to the CSP
        :param variables: set of variables
        :param potential: potential function taking values of the variables as input and returning
        non-negative value of the potential
        """

        if type(variables) not in (list, set): raise ValueError('Variables should be a list or a set.')
        if type(variables) is list: variables = frozenset(variables)

        if variables in self.factors.keys():
            self.factors[variables].append(factor_function)
        else:
            self.factors[variables] = [factor_function]


csp_Scedule = CSP()
csp_Scedule.factors = {}
activities = ['AI',
              'WEB',
              'Leisure']


time_slots = [  # domain
                 (1,8), (1,9), (1,10), (2,8)
]

csp_Scedule.domains_pack = activities

for t in time_slots:
    csp_Scedule.add_variable(t, copy.deepcopy(activities))


def AI_is_done(partial_assignment):
    AI_time = 0
    for t_s in partial_assignment:
        if partial_assignment[t_s] == ['AI']:
            AI_time += 1
    if AI_time < 5:
        return AI_time / 5
    else:
        if AI_time > 5:
            return 1 + (AI_time - 5) / AI_time
        else:
            return 1


def total_positive(partial_assignment):
    return AI_is_done(partial_assignment)


class csp_solver():
    def solve(self, csp, k_best):
        self.csp = csp

        # Dictionary for storing all valid assignments. Note, unlike standard CSP when we
        # are interested only in one valid assignment, for this problem you need to
        # find all valid assignments
        self.current_assignments = []

        # Number of all valid assignments

        # Number of times backtracking operation is called
        self.num_operations = 0

        self.backtrack(copy.deepcopy(csp.assigned_domains), k_best, not_assigned_variables= copy.deepcopy(self.csp.variables))

        if self.current_assignments != []:
            print('Found %d optimal assignments in %d operations' % (len(self.current_assignments), self.num_operations))
            self.current_assignments.sort(key=total_positive)
            for assignment in self.current_assignments:
                print(assignment)
                print(total_positive(assignment))
        else:
            print('No assignments was found.')

    def choose_k_best(self, arr, measure, k):
        arr.sort(key=measure)
        return arr[-k:]

    def update_global_assignments(self, assignments_array):
        final_ass = []

        self.current_assignments.extend(assignments_array)
        self.current_assignments = self.choose_k_best(self.current_assignments, total_positive, 3)



    def backtrack(self, partial_assignment, K_best, not_assigned_variables):

        next_timeslot = self.choose_next_variable(partial_assignment)

        new_assignments = []
        for tasks in self.csp.domains_pack:
            self.num_operations += 1

            updated_assignment = copy.deepcopy(partial_assignment)

            updated_assignment[next_timeslot] = [tasks]

            new_assignments.append(updated_assignment)

        k_best = self.choose_k_best(new_assignments, total_positive, K_best)

        self.update_global_assignments(k_best)

        #k_best = self.remove_full_assignments(k_best)

        if (len(not_assigned_variables) > 0):
            reduced_variables = copy.deepcopy(not_assigned_variables)
            reduced_variables.remove(next_timeslot)
            for assignment in k_best:
                self.backtrack(copy.deepcopy(assignment), K_best, reduced_variables )
        else:
            self.current_assignments = k_best



    def choose_next_variable(self, partial_assignment):  # max domain size

        max_domain_size = 0
        variable_for_partial_assignment = None
        for variable in self.csp.variables: #any variable from variables pack
            if not variable in partial_assignment: # which is not assigned still (but better next in time)
                return variable

    def get_single_value_domains(self, partial_assignment):
        single_assignments_variables = []
        for variable in partial_assignment:
            if (len(partial_assignment[variable]) == 1):
                single_assignments_variables.append(variable)
        return single_assignments_variables

    def diff(self, first, second):
        second = set(second)
        return [item for item in first if item not in second]
    #
    # def forward_checking(self, assigned_variables, partial_assignment, factors):
    #
    #     last_assigned_variable = assigned_variables[len(
    #         assigned_variables) - 1]  # getting last assigned variable, as only its assignment suppose to be unchecked
    #
    #     assigned_value = partial_assignment[last_assigned_variable]
    #
    #     for var in partial_assignment:
    #         if (var in assigned_variables):
    #             continue
    #         partial_assignment[var].remove(assigned_value[0])
    #
    #     if (not self.still_possible(partial_assignment)):
    #         print("CAN'T DO ALL ASSIGNMENTS, DOMAINS ARE OUT")
    #         return None  # case of BAD ASSIGNMENT
    #
    #     single_value_domains = self.get_single_value_domains(partial_assignment)
    #     newly_single_valued = self.diff(single_value_domains, assigned_variables)
    #
    #     if (len(newly_single_valued) != 0):  # situation when we have new auto-assignments
    #         return self.forward_checking(assigned_variables + [newly_single_valued[0]],
    #                                      copy.deepcopy(partial_assignment), factors)
    #     else:
    #         return partial_assignment  # return as it is


solver = csp_solver()
solver.solve(csp_Scedule, 3)