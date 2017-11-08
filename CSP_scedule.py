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


time_slots = [
    (1,16), (1,17), (1,18), (1,19), (1,20), (1, 21),
     (2,9), (2,18), (2,20), (2,21),
 (3,9), (3,18), (3,20), (3,21),
 (4,9), (4,16),(4,17),(4,18),(4,19), (4,21), (4,22),
#
 (5,9), (5,10),(5,11),(5,12),(5,13), (5,14), (5,15), (5,16), (5,17),(5,18),(5,19),(5,20), (5,21),
#
 (6,9), (6,10),(6,11),(6,12),(6,13), (6,14), (6,15), (6,16), (6,17),(6,18),(6,19),(6,20), (6,21),
#
 (7,9), (7,10),(7,11),(7,12),(7,13), (7,14), (7,15), (7,16), (7,17),(7,18),(7,19),(7,20), (7,21)
]

csp_Scedule.domains_pack = activities

for t in time_slots:
    csp_Scedule.add_variable(t, copy.deepcopy(activities))


def AI_is_done(partial_assignment, coef):
    AI_time = 0
    for t_s in partial_assignment:
        if partial_assignment[t_s] == 'AI':
            AI_time += 1
    if AI_time <= 30:
        return AI_time * coef
    else:
        if AI_time > 30:
            return 1 + (AI_time - 30) / AI_time


def Leisure(partial_assignment, coef):
    Leisure = 0
    for t_s in partial_assignment:
        if partial_assignment[t_s] == 'Leisure':
            Leisure += 1
    return Leisure * coef


def no_more_then_4hrs_study_in_a_row(partial_assignment, coef):
    single_study_session_time = 0
    overtime = 0
    for t_s in partial_assignment:
        if partial_assignment[t_s] in ['AI', 'WEB']:
            single_study_session_time+=1
        else:
            single_study_session_time=0
        if (single_study_session_time>4):
            overtime+=1
    return - overtime * coef

def total_positive(partial_assignment):
    return AI_is_done(partial_assignment, 1) + \
           Leisure(partial_assignment, 0.8) + \
           no_more_then_4hrs_study_in_a_row(partial_assignment, 0.2)


class csp_solver():

    def center_string(self, to_print, width, filler = " "):
        return filler * ((width - len(to_print)) // 2) + str(to_print) +  filler * (((width - len(to_print)) + 1) // 2)

    def plot_week(self, assignment):
        week_matrix = [[0 for col in range(7)] for row in range(24)]
        for elements in assignment:
            week_matrix[elements[1]][elements[0]-1] = assignment[elements]
        placeholder = ' __=__ '
        header = ["MON","TUE", "WED", "THS", "FRD", "SAT", "SUN"]
        time = 0
        week_line = self.center_string(" ", len(placeholder), " ") + "  "
        for day in header:
            week_line += self.center_string(day, len(placeholder), " ")
        print(week_line)
        for rows in week_matrix:
            week_line = " " * ((len(placeholder) - len(str(time)))//2) + str(time) + ": " + " " * (((len(placeholder) - len(str(time)))+1)//2)
            for cols in rows:
                if cols != 0:
                    week_line += " " * ((len(placeholder) - len(str(cols)))//2) + str(cols) + " " * (((len(placeholder) - len(str(cols)))+1)//2)
                else:
                    week_line += placeholder
            print(week_line)
            time += 1


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
                self.plot_week(assignment)
                #print(assignment)
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
        for task in self.csp.domains_pack:
            self.num_operations += 1

            updated_assignment = copy.deepcopy(partial_assignment)

            updated_assignment[next_timeslot] = task

            new_assignments.append(updated_assignment)

        k_best = self.choose_k_best(new_assignments, total_positive, K_best)

        self.update_global_assignments(k_best)

        #k_best = self.remove_full_assignments(k_best)

        if (len(not_assigned_variables) > 1):
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
solver.solve(csp_Scedule, 1)
