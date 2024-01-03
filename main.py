import extra
import csp
import time
import sys

###### FUNCTION ######

# Check constraints between A and B variables
def check_con(A, a, B, b):
    if ((A,B) in constraints) and (constraints[(A,B)][1] == '='):
        return (abs(a-b) == constraints[(A,B)][0])
    
    elif ((A,B) in constraints) and (constraints[(A,B)][1] == '>'):
        return (abs(a-b) > constraints[(A,B)][0])
    
    elif ((B,A) in constraints) and (constraints[(B,A)][1] == '='):
        return (abs(a-b) == constraints[(B,A)][0])
    
    elif ((B,A) in constraints) and (constraints[(B,A)][1] == '>'):
        return (abs(a-b) > constraints[(B,A)][0])
        

####### MAIN ########
    
# Input argument that indicates instance file from ./rlfap
instance = sys.argv[1]

# Parsing
variables, var_domain, domains, constraints, neighbors = extra.parsing(instance)

### FC ###
data = csp.CSP(variables, domains, neighbors, check_con, constraints)

print("FC\n")
start = time.time()
fc_result, checks = csp.backtracking_search(data, select_unassigned_variable=csp.domwdeg, order_domain_values=csp.lcv, inference=csp.forward_checking)
end = time.time()
print(fc_result)
print("\nTime elapsed: %.3f" %(end-start), "seconds")
print("\nVisited nodes: %d" % data.nassigns)
print("\nConstraint checks: %d" % checks)

# ### MAC ###
data = csp.CSP(variables, domains, neighbors, check_con, constraints)

print("MAC\n")
start = time.time()
fc_result, checks = csp.backtracking_search(data, select_unassigned_variable=csp.domwdeg, order_domain_values=csp.lcv, inference=csp.mac)
end = time.time()
print(fc_result)
print("\nTime elapsed: %.3f" %(end-start), "seconds")
print("\nVisited nodes: %d" % data.nassigns)
print("\nConstraint checks: %d" % checks)

### FC-CBJ ###
data = csp.CSP(variables, domains, neighbors, check_con, constraints)

print("FC-CBJ\n")
start = time.time()
fc_result, checks = csp.cbj_search(data, select_unassigned_variable=csp.domwdeg, order_domain_values=csp.lcv, inference=csp.forward_checking)
end = time.time()
print(fc_result)
print("\nTime elapsed: %.3f" %(end-start), "seconds")
print("\nVisited nodes: %d" % data.nassigns)
print("\nConstraint checks: %d" % checks)

### MinConflicts ###
data = csp.CSP(variables, domains, neighbors, check_con, constraints)

print("MinConflicts\n")
start = time.time()
fc_result, checks = csp.min_conflicts(data)
end = time.time()
print(fc_result)
print("\nTime elapsed: %.3f" %(end-start), "seconds")
print("\nVisited nodes: %d " % data.nassigns)
print("\nConstraint checks: %d" % checks)
