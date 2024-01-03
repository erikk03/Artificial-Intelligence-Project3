######### Parsing #########

# For rlfap/var files
def rlfap_var(string):
    f = open(string, "r")
    
    var = []                                # List with variables
    var_domain = {}                         # Dictionary with variables(key) and domains(item)
    text = f.readlines()
    for i in text[1:]:                      # Ignore first line
        line = format(i.strip("\n"))        # Take line
        v, d = line.split(" ")              # Split variable and domain
        var.append(int(v))                  # Append variable to list
        var_domain[int(v)] = int(d)         # variable:domain pairs
    
    f.close()

    return var, var_domain

# For rlfap/dom files
def rlfap_dom(string, variables, var_domain):
    f = open(string, "r")
    
    domains = {}
    total = {}                                      # Dictionary with domains(key) and a list with domain's values(item)
    text = f.readlines()
    for i in text[1:]:                              # Ignore first line
        line = format(i.strip("\n"))                # Take line
        str = line.split(" ")                       # Split domain, numOfValues, values
        str = [int(i) for i in str]
        for domain in str[:1]:                      # For each domain
            total[domain] = str[2:]                 # Pair domain with it's values
    
    for var in variables:                           # For each variable
        var_d = var_domain[var]
        domains[var] = total[var_d]       # Pair variable with values of the domain that is paired with this variable
    
    f.close()

    return domains

# For rlfap/ctr files
def rlfap_ctr(string):
    f = open(string, "r")

    constraints = {}                            # Dictionary with pair of variables as tuple(key) and a tuple with "k value" and the opperator(item)
    neighbors = {}                              # Dictionary with variables(key) and a list with all variable's neighbors(item)
    text = f.readlines()
    for i in text[1:]:                          # Ignore first line
        line = format(i.strip(" "))             # Take line
        x, y, operator, k = line.split(" ")     # Split variables x and y, operator, k positive constant
        k = int(k)                              # Convert strs into integers
        x = int(x)
        y = int(y)

        constraints[(x,y)]=(k,operator)         # Pair (x,y) tuple with (k,operator) tuple
        constraints[(y,x)]=(k,operator)         # where key=(x,y) and item=(k,operator). Same for (y,x)
                                                # Update neighbors dictionary
        if x in neighbors:                      # If x variable is a key in neighbors
            neighbors[x].append(y)              # then append y to it's list of neighbors
        else:
            neighbors[x] = []                   # Otherwise create new key
            neighbors[x].append(y)              # and add y to it's list

        if y in neighbors:                      # Same as x
            neighbors[y].append(x)
        else:
            neighbors[y] = []
            neighbors[y].append(x)
    
    f.close()

    return constraints, neighbors

# Does the total parsing calling the functions above
# Returns: variables, var_domain, domains, constraints, neighbors
def parsing(instance):
    variables, var_domain = rlfap_var("rlfap/var" + instance + ".txt")
    domains = rlfap_dom("rlfap/dom" + instance + ".txt", variables, var_domain)
    constraints, neighbors = rlfap_ctr("rlfap/ctr" + instance + ".txt")

    return variables, var_domain, domains, constraints, neighbors