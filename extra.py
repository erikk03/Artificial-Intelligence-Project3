import csp
import sys
from utils import argmin_random_tie, count

#Class to parse data
class Parsing(csp.CSP):
    def __init__(self, file_name):
        #Read variables and domain indexes of CSP
        variables_domain = []
        f = open("rlfap/var"+file_name, "r")
        #Ignore first line
        first_line = f.readline()
        for line in f:
            line = line.strip()
            variables_domain.append(line.split(" "))
        f.close

        #Append variables to a list
        self.variables = []
        for item in variables_domain:
            self.variables.append(int(item[0]))

        #Read the domain indexes and their values
        domains_value = []
        f = open("rlfap/dom"+file_name, "r")
        #Ignore first line
        first_line = f.readline()
        for line in f:
            line = line.strip()
            domains_value.append(line.split(" "))
        
        #Dictionary of {var:[possible_value, ...]} entries
        self.variables_lists_of_values = {}
        #For each domain of a variable, search its value in domains_value list
        for variable_domain in variables_domain:
            list_of_values = []
            for item in domains_value:
                if variable_domain[1] == item[0]:
                    #Ignore the first number and the second number
                    #which are domain index and amount of records
                    for value in item[2:]:
                        list_of_values.append(int(value))
                    self.variables_lists_of_values.update({int(variable_domain[0]): list_of_values})
                    break
        f.close

        # we need a list that contains lists of constrains splitted
        # and a dictionary with the constrains as key and the weight as value for dom/wdeg
        self.constraints_splitted = []
        self.weights = {}
        #Read constraints
        f = open("rlfap/ctr"+file_name, "r")
        #Ignore 1st
        first_line = f.readline()
        for line in f:
            line = line.strip()
            self.weights.update({line: 1})
            self.constraints_splitted.append(line.split(" "))
        f.close

        #A dictionary of {var:[var,...]} that for each variable lists the other var that participate in constraints
        self.neighbors = {}
        for variable in self.variables:
            list_of_neighbors = []
            for constraint in self.constraints_splitted:
                #search if variable participates in whichever of the two parts of the constraint
                if int(constraint[0]) == variable:
                    list_of_neighbors.append(int(constraint[1]))
                if int(constraint[1]) == variable:
                    list_of_neighbors.append(int(constraint[0]))
            self.neighbors.update({variable: list_of_neighbors})

        # A dicitonary which has a tuple of the two variables as key
        #and a list of the constraints splitted, as value
        #Useful for the constraints function, in order to search in O(1)
        #all the constraints between two variables
        self.tuples_constraints = {}
        for constraint in self.constraints_splitted:
            list_of_constraints = self.tuples_constraints.get((int(constraint[0]), int(constraint[1])))
            if list_of_constraints:
                list_of_constraints.append(constraint)
            else:
                list_of_constraints =[]
                list_of_constraints.append(constraint)
                self.tuples_constraints.update({(int(constraint[0]), int(constraint[1])): list_of_constraints})

        # we dont need these enymore
        variables_domain.clear()
        domains_value.clear()

        #Initialize CSP
        csp.CSP.__init__(self, self.variables, self.variables_lists_of_values, self.neighbors, self.check_constraint)
    
    #A function f(A,a,B,b) that returns true
    #if neighbors A,B satisfy the constraint when they have A=a, B=b
    #If false, return the constraint not satisfied(for usage in dom/wget heuristic)
    def check_constraint(self, A, a, B, b):
        #Counter for constraints been checked
        # self.constraints_count  += 1
        #get a list of the constraints splitted between A and B
        list_of_constraints = self.tuples_constraints.get((A,B))
        if list_of_constraints:
            for constraint in list_of_constraints:
                if constraint[2] == ">":
                    if abs(a-b) > int(constraint[3]):
                        continue
                    else:
                        full_constraint = " ".join(constraint)
                        return False, full_constraint
                elif constraint[2] == "=":
                    if abs(a-b) == int(constraint[3]):
                        continue
                    else:
                        full_constraint = " ".join(constraint)
                        return False, full_constraint
        
        #get a list of the constraints splitted between B and A
        list_of_constraints = self.tuples_constraints.get((B,A))
        if list_of_constraints:
            for constraint in list_of_constraints:
                if constraint[2] == ">":
                    if abs(a-b) > int(constraint[3]):
                        continue
                    else:
                        full_constraint = " ".join(constraint)
                        return False, full_constraint
                elif constraint[2] == "=":
                    if abs(a-b) == int(constraint[3]):
                        continue
                    else:
                        full_constraint = " ".join(constraint)
                        return False, full_constraint
        
        return True, 0
    
# dom/wdeg heuristic

def dom_wdeg(assignment, csp):
    return argmin_random_tie([v for v in csp.variables if v not in assignment], key=lambda var: domain_weight_ratio(csp, var, assignment))

# Find the ratio of current domain length and the weights of the constraints the variable participates in

def domain_weight_ratio(csp, var, assignment):
    if csp.curr_domains:
        sum = 0
        neighbors = csp.neighbors.get(var)
        for neighbor in neighbors:
            if neighbor not in assignment:
                constraints = csp.tuples_constraints.get((var, neighbor))
                if constraints:
                    for constraint in constraints:
                        constraint_full = " ".join(constraint)
                        sum += csp.weights.get(constraint_full)
                constraints = csp.tuples_constraints.get((neighbor, var))
                if constraints:
                    for constraint in constraints:
                        constraint_full = " ".join(constraint)
                        sum += csp.weights.get(constraint_full)
        if sum:
            return len(csp.curr_domains[var])/sum
        else:
            return sys.maxsize
        return 
            
    else:
        return count(csp.nconflicts(var, val, assignment) == 0 for val in csp.domains[var])
