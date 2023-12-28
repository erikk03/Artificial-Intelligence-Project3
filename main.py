import extra
import csp
import time

if __name__ == '__main__':
    #For each instance, read the data and run the backtracking search with FC and MAC

    #2-f24#
    print("\n2-f24\n")
    data = extra.Parsing("2-f24.txt")
    print("FC")
    start = time.time()
    # fc_result, constraint_checks, visited_nodes = csp.backtracking_search(data, select_unassigned_variable=csp.dom_wdeg, inference=csp.forward_checking)
    fc_result = csp.backtracking_search(data, csp.mrv, csp.unordered_domain_values, csp.forward_checking)
    end = time.time()
    print(fc_result)
    print("Time elapsed: %.5f" %(end-start), "seconds")
    # print("Constaint checks:", constraint_checks)
    # print("Visited nodes:", visited_nodes)

    data = extra.Parsing("2-f24.txt")
    print("\nMAC")
    start = time.time()
    # mac_result, constraint_checks, visited_nodes = csp.backtracking_search(data, select_unassigned_variable=csp.dom_wdeg, inference=csp.mac)
    mac_result = csp.backtracking_search(data, csp.mrv, csp.unordered_domain_values, csp.mac)
    end = time.time()
    print(fc_result)
    print("Time elapsed: %.5f" %(end-start), "seconds")
    # print("Constaint checks:", constraint_checks)
    # print("Visited nodes:", visited_nodes)

    data = extra.Parsing("2-f24.txt")
    print("\nMin Conflicts")
    start = time.time()
    minConflicts_result = csp.min_conflicts(data)
    end = time.time()
    print(minConflicts_result)
    print("Time elapsed: %.5f" % (end - start), "seconds")