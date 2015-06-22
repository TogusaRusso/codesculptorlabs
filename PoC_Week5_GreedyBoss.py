"""
Simulator for greedy boss scenario
"""

import simpleplot
import math
import codeskulptor
codeskulptor.set_timeout(20)

STANDARD = True
LOGLOG = False

# constants for simulation
INITIAL_SALARY = 100
SALARY_INCREMENT = 100
INITIAL_BRIBE_COST = 1000


def greedy_boss(days_in_simulation, bribe_cost_increment, plot_type = STANDARD):
    """
    Simulation of greedy boss
    """
    
    # initialize necessary local variables
    
    current_day = 0
    total_salary = 0
    savings = 0
    bribe_cost = INITIAL_BRIBE_COST
    salary = INITIAL_SALARY
    
    # initialize list consisting of days vs. total salary earned for analysis
    days_vs_earnings = [(0, 0)]

    # Each iteration of this while loop simulates one bribe
    while current_day <= days_in_simulation:
        
        # check whether we have enough savings to bribe without waiting
        time_to_bribe = max([0, 
                             int(math.ceil((bribe_cost - savings) 
                                           / float(salary)))]) 
        
        
        # advance current_day to day of next bribe (DO NOT INCREMENT BY ONE DAY)
        
        current_day += time_to_bribe

        # update state of simulation to reflect bribe
        savings += salary * time_to_bribe - bribe_cost
        total_salary += salary * time_to_bribe
        bribe_cost += bribe_cost_increment
        salary += SALARY_INCREMENT
        
        

        # update list with days vs total salary earned for most recent bribe
        # use plot_type to control whether regular or log/log plot
        
        if plot_type == STANDARD:
            days_vs_earnings.append((current_day, total_salary))
        elif plot_type == LOGLOG:
            days_vs_earnings.append((math.log(current_day), math.log(total_salary)))
       
        
   
    return days_vs_earnings


def run_simulations():
    """
    Run simulations for several possible bribe increments
    """
    plot_type = LOGLOG
    days = 120
    inc_0 = greedy_boss(days, 0, plot_type)
    graph_1 = []
    graph_2 = []
    graph_3 = []
    graph_4 = []
    for point in inc_0:
        d = math.exp(point[0])
        graph_1.append((point[0], math.log(math.exp(0.095 * d))))
        #graph_2.append((point[0], math.log(95 * d * d)))
        #graph_3.append((point[0], math.log(math.exp(9.5 * d))))
        #graph_4.append((point[0], math.log(9.5 * d * d * d *d)))
    
    #inc_500 = greedy_boss(days, 500, plot_type)
    #inc_1000 = greedy_boss(days, 1000, plot_type)
    #inc_2000 = greedy_boss(days, 2000, plot_type)
#    simpleplot.plot_lines("Greedy boss", 600, 600, "days", "total earnings", 
#                          [inc_0, inc_500, inc_1000, inc_2000], False,
#                         ["Bribe increment = 0", "Bribe increment = 500",
#                          "Bribe increment = 1000", "Bribe increment = 2000"]
#                         )
    simpleplot.plot_lines("Greedy boss", 600, 600, "days", "total earnings", 
                          [inc_0, graph_1], False,
                         ["Bribe increment = 0", "graph_1"]
                         )
    x1 = -1
    y1 = -1
    #for point in inc_0:
    #    print (point[1] - y1) / (point[0] - x1)
    #    y1 = point[1]
    #    x1 = point[0]

run_simulations()

print 1.15 ** 0

#print greedy_boss(50, 1000)

#for point in greedy_boss(50, 1000):
#    d = point[0]
#    print d, point[1], 5 * d**2  + 50*d


#print greedy_boss(35, 100)
# should print [(0, 0), (10, 1000), (16, 2200), (20, 3400), (23, 4600), (26, 6100), (29, 7900), (31, 9300), (33, 10900), (35, 12700), (37, 14700)]

#print greedy_boss(35, 0)
# should print [(0, 0), (10, 1000), (15, 2000), (19, 3200), (21, 4000), (23, 5000), (25, 6200), (27, 7600), (28, 8400), (29, 9300), (30, 10300), (31, 11400), (32, 12600), (33, 13900), (34, 15300), (34, 15300), (35, 16900), (36, 18600)]
    