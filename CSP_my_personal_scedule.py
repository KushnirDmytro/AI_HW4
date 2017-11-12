import copy
import time


# ========================= INTRO =====================
class CSP(object):
    def __init__(self):
        self.variables = []
        self.domain = {}
        self.previous_assignments_level = [{}]
        self.current_level_assignments = []
        self.this_level_number = 0
        self.last_variable_index = -1

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
        self.last_variable_index += 1


csp_Scedule = CSP()
csp_Scedule.factors = {}
activities = ['AI',
                'IoT',
              'WEB',
              'Sports',

              'Projects',
              'Games',

              'DS_club',
              'ALGO_club',
              'Ethics'
              ]
study_activities = ['AI',
                    'IoT',
                    'Ethics'
                    'WEB',
                    'Projects',
                    'DS_club',
                    'ALGO_club']

long_study_activities = ['AI',
                    'Ethics'
                    'IoT',
                    'WEB',
                    'Projects']

time_slots = [
    # workdays with lectures
    (1, 14),(1, 15),(1, 16), (1, 17), (1, 18), (1, 19), (1, 20), (1, 21), (1, 22), (1, 23), (2, 0), (2, 1), (2, 2),
    (2, 14), (2, 15), (2, 16), (2, 21), (2, 22), (2, 23), (3, 0), (3, 1), (3, 2), #have late study session from 17PM on tuesday
    (3, 14), (3, 15), (3, 16),(3, 17),(3, 18), (3, 20), (3, 21), (3, 22), (3, 23), (4, 0), (4, 1), (4, 2),
    (4, 12), (4, 13), (4, 14), (4, 15),(4, 16), (4, 17), (4, 18), (4, 19), (4, 21), (4, 22), (4, 23), (5, 0), (5, 1), (5, 2),

    # workdays without lectures
    (5, 10), (5, 11), (5, 12), (5, 13), (5, 14), (5, 15), (5, 16), (5, 17), (5, 18), (5, 19), (5, 20), (5, 21),
    (5, 22), (5, 23),(6, 0), (6, 1),(6, 2),(6, 3),
    (6, 10), (6, 11), (6, 12), (6, 13), (6, 14), (6, 15), (6, 16), (6, 17), (6, 18), (6, 19), (6, 20), (6, 21),
    (6, 22), (6, 23),(7, 0),(7, 1),
    (7, 10), (7, 11), (7, 12), (7, 13), (7, 14), (7, 15), (7, 16), (7, 17), (7, 18), (7, 19), (7, 20), (7, 21),(7, 22),(7, 23),(1,0), (1,1)
]

csp_Scedule.domain = activities

for t in time_slots:
    csp_Scedule.add_variable(t, [])


# ========================= /INTRO =====================

class csp_solver():
    # =========================UTILS==========================
    def choose_next_variable(self, partial_assignment):  # max domain size

        max_domain_size = 0
        variable_for_partial_assignment = None
        for variable in self.csp.variables:  # any variable from variables pack
            if not variable in partial_assignment:  # which is not assigned still (but better next in time)
                return variable

    def lists_diff(self, first, second):
        second = set(second)
        return [item for item in first if item not in second]

    # ===========================/UTILS==========================

    # ==================== FOR OUTPUT =================


    def center_string(self, to_print, width, filler=" "):
        return filler * ((width - len(to_print)) // 2) + str(to_print) + filler * (((width - len(to_print)) + 1) // 2)

    def plot_week(self, assignment):
        week_matrix = [[0 for col in range(7)] for row in range(24)]
        for elements in assignment:
            week_matrix[elements[1]][elements[0] - 1] = assignment[elements]
        placeholder = ' ___=___ '
        header = ["MON", "TUE", "WED", "THS", "FRD", "SAT", "SUN"]
        time = 0
        week_line = self.center_string(" ", len(placeholder), " ") + "  "
        for day in header:
            week_line += self.center_string(day, len(placeholder), " ")
        print(week_line)
        for rows in week_matrix:
            week_line = " " * ((len(placeholder) - len(str(time))) // 2) + str(time) + ": " + " " * (
            ((len(placeholder) - len(str(time))) + 1) // 2)
            for cols in rows:
                if cols != 0:
                    week_line += " " * ((len(placeholder) - len(str(cols))) // 2) + str(cols) + " " * (
                    ((len(placeholder) - len(str(cols))) + 1) // 2)
                else:
                    week_line += placeholder
            print(week_line)
            time += 1
            # ==================== /FOR OUTPUT =================

            # =====================SOLVER PART ==================

    def solve(self, csp, k_best):
        self.csp = csp
        self.current_assignments = []
        self.num_operations = 0

        exec_start = time.process_time()
        self.backtrack(  # not_assigned_variables= copy.deepcopy(self.csp.variables),
            K_best=k_best,
            depth=0,
            work_with_node_in_prev_layer=0,
            next_variable_index=0)
        exec_end = time.process_time()
        exec_time = exec_end - exec_start

        self.current_assignments = self.choose_k_best(self.csp.current_level_assignments, total_satisfaction, k_best)

        if self.current_assignments != []:
            print('Found %d optimal assignments in %d operations time %d seconds' % (
            len(self.current_assignments), self.num_operations, exec_time))
            self.current_assignments.sort(key=total_satisfaction)
            for assignment in self.current_assignments:
                self.plot_week(assignment)
                print("Satisfaction: " + str(total_satisfaction(assignment)))
        else:
            print('No assignments was found.')

    def choose_k_best(self, arr, measure, k):
        # for border cases
        if len(arr) <= k:
            return arr

        # caching values of heuristics
        cache_arr = []
        cache_indx = 0
        for el in arr:
            cache_arr.append((measure(el), cache_indx))
            cache_indx += 1
        cache_arr.sort(key=lambda x: x[0], reverse=True)
        result = []
        for best_index in range(k):
            result.append(arr[(cache_arr[best_index])[1]])
        return result

    def backtrack(self, K_best, depth, work_with_node_in_prev_layer, next_variable_index):

        # next_timeslot = self.choose_next_variable(partial_assignment)
        next_timeslot = self.csp.variables[
            next_variable_index]  # just faster, have no argument why consequent assignment is bad

        # if we've started new tree layer, update for this node
        if (depth > self.csp.this_level_number):
            self.csp.previous_assignments_level = self.choose_k_best(self.csp.current_level_assignments,
                                                                     total_satisfaction, K_best)
            self.csp.current_level_assignments = []
            self.csp.this_level_number = depth

        # Try all possible assignmtnts for this worker's node
        for task in self.csp.domain:
            self.num_operations += 1
            updated_assignment = copy.deepcopy(self.csp.previous_assignments_level[work_with_node_in_prev_layer])
            updated_assignment[next_timeslot] = task
            self.csp.current_level_assignments.append(updated_assignment)

        # last node in workers layer
        if depth == 0 or (work_with_node_in_prev_layer == len(self.csp.previous_assignments_level) - 1):
            if (next_variable_index < self.csp.last_variable_index - 1):

                next_level_worker_numbers = min(K_best, len(self.csp.current_level_assignments))
                for node_in_next_layer in range(next_level_worker_numbers):
                    self.backtrack(K_best, depth + 1, node_in_next_layer, next_variable_index + 1)


# =================================== /SOLVER =====================================



# ================================= /HEURISTICS =========================================

def AI_is_done(partial_assignment, Avarage_time, coef):
    AI_time = 0
    for t_s in partial_assignment:
        if partial_assignment[t_s] == 'AI':
            AI_time += 1
    if AI_time <= Avarage_time:
        return AI_time * coef
    else:
        if AI_time > Avarage_time:
            return count_suboptimal_with_overrun_limitless(current_value=AI_time,
                                                           optimal_value=Avarage_time) * coef  # extra study costs less and less


def Ethics_is_done(partial_assignment, Avarage_time, coef):
    Ethics_time = 0
    for t_s in partial_assignment:
        if partial_assignment[t_s] == 'Ethics':
            Ethics_time += 1
    if Ethics_time <= Avarage_time:
        return Ethics_time * coef
    else:
        if Ethics_time > Avarage_time:
            return count_suboptimal_with_overrun_limitless(current_value=Ethics_time,
                                                           optimal_value=Avarage_time) * coef  # extra study costs less and less


def IoT_is_done(partial_assignment, Avarage_time, coef):
    IoT_time = 0
    for t_s in partial_assignment:
        if partial_assignment[t_s] == 'IoT':
            IoT_time += 1
    if IoT_time <= Avarage_time:
        return IoT_time * coef
    else:
        if IoT_time > Avarage_time:
            return count_suboptimal_with_overrun_limitless(current_value=IoT_time,
                                                           optimal_value=Avarage_time) * coef  # extra study costs less and less


def WEB_is_done(partial_assignment, Avarage_time, coef):
    WEB_time = 0
    for t_s in partial_assignment:
        if partial_assignment[t_s] == 'WEB':
            WEB_time += 1
    if WEB_time <= Avarage_time:
        return WEB_time * coef
    else:
        if WEB_time > Avarage_time:
            return count_suboptimal_with_overrun_limitless(current_value=WEB_time,
                                                           optimal_value=Avarage_time) * coef  # extra study costs less and less


def Free_choice(partial_assignment, coef):
    Leisure = 0
    for t_s in partial_assignment:
        if partial_assignment[t_s] in ['Sports', 'Games']:
            Leisure += 1
    return Leisure * coef


def no_more_then_4hrs_study_in_a_row(partial_assignment, coef):
    single_study_session_time = 0
    previous_time_slot = (0, 0)  # init value
    overtime = 0
    for t_s in partial_assignment:
        this_time_slot = partial_assignment[t_s]

        # checking for natural breaks in timeline
        if t_s[1] != previous_time_slot[1] + 1 or t_s[0] != previous_time_slot[0]:
            single_study_session_time = 0

        if this_time_slot in study_activities:
            single_study_session_time += 1
        else:
            single_study_session_time = 0
        if (single_study_session_time > 4):
            overtime += 1
        previous_time_slot = t_s  # memorising after processing
    return - overtime * coef


def daily_overtime(partial_assignment, coef):
    whole_day_study_time = 0
    previous_time_slot = (0, 0)  # init value
    overtime = 0
    for t_s in partial_assignment:
        this_time_slot = partial_assignment[t_s]

        # checking for natural breaks in timeline
        if t_s[0] != previous_time_slot[0]:  # if day changed
            whole_day_study_time = 0

        if this_time_slot in study_activities:
            whole_day_study_time += 1
        if (t_s[0] < 5 and (whole_day_study_time > 4)) or (whole_day_study_time > 8):
            overtime += 1
        previous_time_slot = t_s  # memorising after processing

    return -overtime * coef


def visit_DS_club(partial_assignment, DS_clutb_time, coef):
    if (DS_club_time in partial_assignment) and partial_assignment[DS_clutb_time] == 'DS_club':
        return coef
    else:
        return 0


def visit_ALGO_club(partial_assignment, ALGO_club_time, coef):
    if (ALGO_club_time in partial_assignment) and partial_assignment[ALGO_club_time] == 'ALGO_club':
        return coef
    else:
        return 0


def is_not_a_Time_for_sports(partial_assignment, coef, time_From, time_To):
    sports_not_in_time = 0
    for t_s in partial_assignment:
        this_time_slot = partial_assignment[t_s]

        if this_time_slot == 'Sports' and (t_s[1] > time_To or t_s[1] < time_From) and (t_s[0] < 5):
            sports_not_in_time += 1
    return - coef * sports_not_in_time


def being_healthy_sport(partial_assignment, optimal_time, coef):
    weekly_sport = 0
    for t_s in partial_assignment:
        this_time_slot = partial_assignment[t_s]

        if this_time_slot == 'Sports':
            weekly_sport += 1

    if weekly_sport <= optimal_time:
        return weekly_sport * coef
    else:
        return count_suboptimal_with_overrun_limitless(current_value=weekly_sport,
                                                       optimal_value=optimal_time) * coef


def count_suboptimal_with_overrun_limitless(current_value, optimal_value):
    return (optimal_value +  # base, optimal part
            (current_value - optimal_value) *  # additional value
            (current_value - (
                current_value - optimal_value)) / current_value)  # it's role decreases with increasing of difference


def Project_progress(partial_assignment, coef):
    optional_tasks = 0
    for t_s in partial_assignment:
        this_time_slot = partial_assignment[t_s]

        if this_time_slot == 'Projects':
            optional_tasks += 1

    return optional_tasks * coef


def playing(partial_assignment, optimal_time, undesirable_time, coef):
    weekly_games = 0
    for t_s in partial_assignment:
        this_time_slot = partial_assignment[t_s]

        if this_time_slot == 'Games':
            weekly_games += 1

    if weekly_games <= optimal_time:
        return weekly_games * coef
    else:
        if weekly_games <= undesirable_time:
            return count_suboptimal_with_overrun_limitless(current_value=weekly_games,
                                                           optimal_value=optimal_time) * coef
        else:
            return count_suboptimal_with_overrun_limitless(current_value=weekly_games,
                                                           optimal_value=optimal_time / 2) * coef


def game_addictivity(partial_assignment, game_addictivity_period, coef):  # 1 hr usually only increases wish to play on
    gaming_hrs_in_a_row = 0
    previous_time_slot = (-1, -1)  # init value

    satisfaction = 0

    for t_s in partial_assignment:
        this_time_slot = partial_assignment[t_s]

        # checking for natural breaks in timeline
        if t_s[1] != previous_time_slot[1] + 1 or t_s[0] != previous_time_slot[0]:
            gaming_hrs_in_a_row = 0

        if partial_assignment[t_s] == "Games":
            gaming_hrs_in_a_row += 1
        else:
            gaming_hrs_in_a_row = 0

        if (gaming_hrs_in_a_row <= game_addictivity_period):
            satisfaction += gaming_hrs_in_a_row * coef / game_addictivity_period  # rising up to 1 * coef
        else:
            satisfaction -= (
                            gaming_hrs_in_a_row - game_addictivity_period) * coef / game_addictivity_period * 2  # from 0 down to - inf

        previous_time_slot = t_s  # memorising after processing

    return satisfaction * coef

def try_to_finish_what_have_started(partial_assignment, continuity_bonus):
    '''
    :return: represents, that continuing previous study task is more preferable, then starting a new one
    '''
    previous_study_time_slot = (-1, -1)  # init value

    satisfaction = 0

    for t_s in partial_assignment:
        this_time_slot_task = partial_assignment[t_s]

        if this_time_slot_task in long_study_activities:
            if (previous_study_time_slot in partial_assignment) and\
                    (partial_assignment[previous_study_time_slot] == this_time_slot_task):
                satisfaction += continuity_bonus

            previous_study_time_slot = t_s  # memorising after processing

    return satisfaction
# ======================== /HEURISTICS =========================

# call


'''TODO
Tune coeficients if You want to check the model <=============================================
'''
AI_avarage_time = 20
WEB_avarage_time = 20
IoT_avarage_time = 10
Ethics_avarage_time = 5
obligatory_tasks = 1
study_continuity_bonus = obligatory_tasks*0.5
Projects_importance = obligatory_tasks * 0.75
not_doing_obligatory = obligatory_tasks / 5
weaknes = 0.8
health_importance = weaknes
enought_time_for_sport = 7
gaming_satisfaction = 0.5  # 1.1
game_addictivity_period = 3
enoght_time_for_games = enought_time_for_sport
really_enoght_time_for_games = enoght_time_for_games * 2  # true..
daily_tiredness = 0.2
DS_club_time = (1, 19)
ALGO_club_time = (3, 18)
DS_club_visiting = obligatory_tasks * 2
ALGO_club_visiting = obligatory_tasks * 2
sports_not_in_time_happines_withdraw = obligatory_tasks
sport_time_from = 17
sport_time_to = 22



def total_satisfaction(partial_assignment):
    return AI_is_done(partial_assignment, Avarage_time=AI_avarage_time, coef=obligatory_tasks) + \
           WEB_is_done(partial_assignment, Avarage_time=WEB_avarage_time, coef=obligatory_tasks) + \
           IoT_is_done(partial_assignment, Avarage_time=IoT_avarage_time, coef=obligatory_tasks) + \
           Ethics_is_done(partial_assignment, Avarage_time=Ethics_avarage_time, coef=obligatory_tasks) + \
           Free_choice(partial_assignment, coef=not_doing_obligatory) + \
           try_to_finish_what_have_started(partial_assignment, continuity_bonus=study_continuity_bonus) + \
           no_more_then_4hrs_study_in_a_row(partial_assignment, coef=weaknes) + \
           daily_overtime(partial_assignment, coef=daily_tiredness) + \
           being_healthy_sport(partial_assignment, optimal_time=enought_time_for_sport, coef=health_importance) + \
           playing(partial_assignment, optimal_time=enought_time_for_sport,
                   undesirable_time=really_enoght_time_for_games, coef=gaming_satisfaction) + \
           Project_progress(partial_assignment, coef=Projects_importance) + \
           visit_DS_club(partial_assignment, coef=DS_club_visiting, DS_clutb_time=DS_club_time) + \
           visit_ALGO_club(partial_assignment, coef=ALGO_club_visiting, ALGO_club_time=ALGO_club_time) + \
           is_not_a_Time_for_sports(partial_assignment, coef=sports_not_in_time_happines_withdraw,
                                 time_From=sport_time_from, time_To=sport_time_to) + \
           game_addictivity(partial_assignment, game_addictivity_period=game_addictivity_period,
                            coef=gaming_satisfaction)  # made to show how it is difficult to stop after single hour


solver = csp_solver()
solver.solve(csp_Scedule,50)
