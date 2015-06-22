"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0
#SIM_TIME = 1000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._cookies_total = 0.0
        self._cookies = 0.0
        self._time = 0.0
        self._cps = 1.0
        self._history =  [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        answer = "Time: " + str(self._time) + "\n"
        answer += "Current Cookies: " + str(self._cookies) + "\n"
        answer += "CPS: " + str(self._cps) + "\n"
        answer += "Total Cookies: " + str(self._cookies_total)
        return answer
     
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        est_time = (cookies - self._cookies) 
        return max([0.0, math.ceil(est_time / self._cps)])
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0:
            self._time += time
            self._cookies += time * self._cps
            self._cookies_total += time * self._cps
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost <= self._cookies:
            self._cookies -= cost
            self._cps += additional_cps
            self._history.append((self._time, item_name, cost, self._cookies_total))
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    # Replace with your code
    build = build_info.clone()
    clicker = ClickerState()
    while clicker.get_time() <= duration:
        item = strategy(clicker.get_cookies(), clicker.get_cps(), 
                        clicker.get_history(), 
                        duration - clicker.get_time(),
                        build)
        if item == None:
            break
        else:
            time = clicker.time_until(build.get_cost(item))
            if time > duration - clicker.get_time():
                break
            else:
                clicker.wait(time)
                clicker.buy_item(item, build.get_cost(item), build.get_cps(item))
                build.update_item(item)
    clicker.wait(duration - clicker.get_time())
    return clicker


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    cheap_item = None
    cheap_cost = 0
    budget = cookies + cps * time_left
    for item in build_info.build_items():
        cost = build_info.get_cost(item)
        if cheap_item == None or cost < cheap_cost:
            if cost <= budget:
                cheap_cost = cost
                cheap_item = item
    return cheap_item

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    exp_item = None
    exp_cost = -1
    budget = cookies + cps * time_left
    for item in build_info.build_items():
        cost = build_info.get_cost(item)
        if cost <= budget and cost > exp_cost:
            exp_cost = cost
            exp_item = item
    return exp_item

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    best_item = None
    best_value = 0 
    budget = cookies + cps * time_left
    for item in build_info.build_items():
        cost = build_info.get_cost(item)
        if cost <= budget:
            #time_to_buy = cost / cps
            add_cps = build_info.get_cps(item)
            value = add_cps / cost
            #sum = (time_left -  time_to_buy) * add_cps - cost
            if value > best_value:
                best_value = value
                best_item = item
    return best_item
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    #history = state.get_history()
    #history = [(item[0], item[3]) for item in history]
    #simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()
 

