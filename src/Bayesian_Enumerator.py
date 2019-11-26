import xml_to_bn as xml

#params:
#   X = query X. 1 symbol: str/char
#   evidence = as many variables as are provided as initial evidence. i number of symbols: dict
#   bn = bayesian network, represented by unordered list
#   varList = list of variables in topological order
def enumerateAsk(X, evidence, bn, varList):
    #Q is the distribution which in our case will only have 1 element
    Q = None #will be a single float value
    # would be a forloop if we didn't have the prerequisite that the query can only be one variable
    evidence[X] = True

    Q = enumerateAll(bn, evidence, varList)

#takes params list representation of bayesian network bn, and evidence e
def enumerateAll(bn, e, vars):
    if vars == []:
        return 1

    print(vars[0])
    #if current variable from list is in the evidence
    if vars[0] in e.keys():
        truthValueList = []

        # get the value of y that is in the evidence
        y = (vars[0], e[vars[0]])

        #XML order of probabilities is reversed
        #add truth value in REVERSE, so T = 0, F = 1
        if y[1] is True:
            truthValueList.append('0')
        else:
            truthValueList.append('1')

        #grab parents of y
        parentsY = []
        currQueryNode = None
        for item in bn:
            if item.name == y[0]:
                currQueryNode = item
                parentsY = item.parent
                break

        #grab truth values of parents of y
        for item in parentsY:
            #to make sure to get rid of root node from probability distribution
            if item.name == 'root':
                break
            # XML order of probabilities is reversed
            # add truth value in REVERSE, so T = 0, F = 1
            if item.value is True:
                truthValueList.append('0')
            else:
                truthValueList.append('1')
        print('truth value list ', truthValueList)

        #grab the decimal representation of this binary number
        decVal = int(''.join(truthValueList), 2)

        #grab the decVal-th element from the list
        ithProbability = currQueryNode.probs[decVal]
        print(ithProbability)

    else:
        pass

# global scope variables from the xml parser
def main():
    start = xml.bayesian_network('root')
    tree = xml.ET.parse('aima-alarm1.xml')
    root = tree.getroot()
    test = xml.make_nodes(root)
    networkList = xml.make_network(root, test, start)

    # topologically ordered list of nodes
    postOrderNodes = xml.linearize(networkList)
    postOrderNodesCut = postOrderNodes[1:]  # the entire list of nodes minus the root node

    # postOrderList is JUST A LIST OF NODE NAMES, NOT NODE OBJECTS
    postOrderList = xml.get_var_names(postOrderNodes)
    postOrderListCut = postOrderList[1:] #the entire list of nodes minus the root node

    enumerateAsk('B', {'B':True, 'C':False}, postOrderNodesCut, postOrderListCut)

main()