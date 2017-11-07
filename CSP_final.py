class CSP(object):
    def __init__(self):
        self.variables = []
        self.domains = {}
        self.factors = {}

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


csp_Australia = CSP()
provinces = ['WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T']
neighbors = {
    'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
    'NT': ['WA', 'Q'],
    'NSW': ['Q', 'V']
}

colors = ['red', 'blue', 'green']


def are_neighbors(a, b):
    return (a in neighbors and b in neighbors[a]) or (b in neighbors and a in neighbors[b])


for p in provinces:
    csp_Australia.add_variable(p, colors)
for p1 in provinces:
    for p2 in provinces:
        if are_neighbors(p1, p2):
            # Neighbors cannot have the same color
            csp_Australia.add_factor([p1, p2], lambda x, y: x != y)

import copy


class csp_solver():
    def solve(self, csp):
        self.csp = csp

        # Dictionary for storing all valid assignments. Note, unlike standard CSP when we
        # are interested only in one valid assignment, for this problem you need to
        # find all valid assignments
        self.valid_assignments = []

        # Number of all valid assignments

        # Number of times backtracking operation is called
        self.num_operations = 0

        self.backtrack(copy.deepcopy(csp.domains))

        if self.valid_assignments != []:
            print('Found %d optimal assignments in %d operations' % (len(self.valid_assignments), self.num_operations))
            for assignment in self.valid_assignments:
                print(assignment)
        else:
            print('No assignments was found.')

    def backtrack(self, partial_assignment):
        """

        2c.

        Here you will implement backtracking search with arc consistency (advanced forward checking) and without propagation
        through a singleton domain for a good reason.

        Backtracking search will work like the following: it takes partial assignment is a form of
        all possible values to the variables (initially - full domains of the CSP). Next, we will do assignments
        by eliminating everything except the assigned value from the variable's domain. This way, we already enforce
        Prop-1 by design.

        If the valid assignment is found, add it to self.valid_assignments in a form of (assignment:}

        :param partial_assignment: a dictionary containing partial assignment in a form {variable:list of possible values}
        """
        # -------- YOUR CODE HERE ----------

        updated_assignment = partial_assignment
        var_to_be_assigned = self.choose_next_variable(updated_assignment)
        var_to_be_assigned = self.choose_next_variable2(updated_assignment)
        for color in partial_assignment[var_to_be_assigned]:
            self.num_operations += 1
            updated_assignment[var_to_be_assigned] = [color]  # reducing domain of assignments
            single_values_domain = self.get_single_value_domains(updated_assignment)
            single_values_domain.remove(var_to_be_assigned)
            single_values_domain.append(var_to_be_assigned)  # place in the end of a list
            new_assignment = self.forward_checking(single_values_domain, copy.deepcopy(updated_assignment),
                                                   self.csp.factors)
            if (new_assignment != None):
                self.backtrack(copy.deepcopy(new_assignment))

    def choose_next_variable(self, partial_assignment):
        """

        2a.

        As Prop-1 is already implemented, we will use different heuristics and return the variable with the _largest_ domain.
        :param partial_assignment: a dictionary containing partial assignment in a form {variable:list of values}
        :return: variable for partial assignment
        """
        # -------- YOUR CODE HERE ----------
        max_domain_size = 0
        variable_for_partial_assignment = None
        for variable in partial_assignment:
            if (len(partial_assignment[variable]) > max_domain_size):
                max_domain_size = len(partial_assignment[variable])
                variable_for_partial_assignment = variable
        return variable_for_partial_assignment

    def choose_next_variable2(self, partial_assignment):
        """

        2a.

        As Prop-1 is already implemented, we will use different heuristics and return the variable with the _largest_ domain.
        :param partial_assignment: a dictionary containing partial assignment in a form {variable:list of values}
        :return: variable for partial assignment
        """
        # -------- YOUR CODE HERE ----------
        min_domain_size = 999999
        variable_for_partial_assignment = None
        for variable in partial_assignment:
            if 1 < len(partial_assignment[variable]) < min_domain_size:
                min_domain_size = len(partial_assignment[variable])
                variable_for_partial_assignment = variable
        return variable_for_partial_assignment

    def all_factors_ok(self, factors, x, y):
        res = True
        for facs in factors:
            res = facs(x, y)
            if (not res):
                return res
        return res

    def still_possible(self, partial_assignment):
        '''
        :param partial_assignment: DICT of values(keys) and possible domain values
        :return: BOOLEAN if this assignment contains empty domains
        '''
        for variable in partial_assignment:
            if (not len(partial_assignment[variable]) > 0):
                return False
        return True

    def is_final_assignment(self, partial_assignment):
        '''
        check is this assignment still need to be simplified
        :param partial_assignment:
        :return: BOOLEAN if all assignments have only 1 final domain
        '''
        if (self.still_possible(partial_assignment)):
            for variable in partial_assignment:
                if (not len(partial_assignment[variable]) != 1):
                    return False
            return True

    def get_single_value_domains(self, partial_assignment):
        single_assignments_variables = []
        for variable in partial_assignment:
            if (len(partial_assignment[variable]) == 1):
                single_assignments_variables.append(variable)
        return single_assignments_variables

    def diff(self, first, second):
        second = set(second)
        return [item for item in first if item not in second]

    def forward_checking(self, assigned_variables, partial_assignment, factors):
        """
                2b.

                Implements forward checking on steroids. Checks if any domain contains values inconsistent with current assignment
                and eliminate these variables from the domain. As a result of this domain reduction there could be another
                inconsistency in the domains. Eliminate them recursively by keeping track of the reduced domain and calling forward_checking
                as a recursion.

                This wild version of forward checking is called arc consistency and is one of the most efficient implementation of the
                forward checking idea for CSP.

                :param assigned_variable: recently assigned variable or the variable for which the domain has been reduced
                :param partial_assignment: a dictionary containing partial assignment in a form {variable:list of values}
                :param factors: a dictionary containing factoors of the CSP if the form of {frozenset(variables):list of constraint functions}
                :return: a dictionary of partial assignments with reduced domains
                """
        last_assigned_variable = assigned_variables[len(
            assigned_variables) - 1]  # getting last assigned variable, as only its assignment suppose to be unchecked
        for fac in factors:
            if (last_assigned_variable in fac):
                # following is for general case when factor function can count more then 2 variables
                for factor_participant in fac:  # crossing out all states which are forbidden for assignment now
                    if (factor_participant == last_assigned_variable):  # skipping our factor
                        continue
                    partial_assignment[factor_participant] = [x for x in partial_assignment[factor_participant] if
                                                              (self.all_factors_ok(factors=factors[fac],
                                                                                   x=x,
                                                                                   y=partial_assignment[
                                                                                       last_assigned_variable][0]
                                                                                   # getting assignment from list of 1 elem
                                                                                   ))
                                                              ]  # filtering the array to cross out

        if (not self.still_possible(partial_assignment)):
            return None  # case of BAD ASSIGNMENT
        single_value_domains = self.get_single_value_domains(partial_assignment)

        newly_single_valued = self.diff(single_value_domains, assigned_variables)

        if (len(newly_single_valued) != 0):  # situation when we have new auto-assignments
            return self.forward_checking(assigned_variables + [newly_single_valued[0]],
                                         copy.deepcopy(partial_assignment), factors)
        else:
            if (len(partial_assignment) == len(single_value_domains)):
                self.valid_assignments.append(partial_assignment)
                return None  # case when we have no new assignments and all our variables have single domains
            else:
                return partial_assignment  # return as it is


solver = csp_solver()
solver.solve(csp_Australia)
