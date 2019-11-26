import xml_to_bn as xml
import copy

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
    return Q

#takes params list representation of bayesian network bn, and evidence e
def enumerateAll(bn, e, vars):
    print('currently passed vars ', vars)
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

        print(' ith prob ', ithProbability)

        return ithProbability*enumerateAll(bn, e, vars[1:])

    else:
        #truth value lists for each respective possible value of y
        # XML order of probabilities is reversed
        # add truth value in REVERSE, so T = 0, F = 1
        truthValueList1 = ['0']
        truthValueList2 = ['1']

        #grab parents of y
        parentsY = []
        currQueryNode = None
        for item in bn:
            if item.name == vars[0]:
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
                truthValueList1.append('0')
                truthValueList2.append('0')
            else:
                truthValueList1.append('1')
                truthValueList2.append('1')
        print('truth value list 1', truthValueList1, ' truth value list 2 ', truthValueList2)

        #grab the decimal representation of this binary number
        decVal1 = int(''.join(truthValueList1), 2)
        decVal2 = int(''.join(truthValueList2), 2)

        #grab the decVal-th element from the list
        print('dec val 1 ', decVal1, 'dec val 2 ', decVal2)
        ithProbability1 = currQueryNode.probs[decVal1]
        ithProbability2 = currQueryNode.probs[decVal2]
        print('ith prob 1 ', ithProbability1, 'ith prob 2 ', ithProbability2)

        #add y value to the evidence
        e1 = copy.deepcopy(e)
        e2 = copy.deepcopy(e)

        e1[vars[0]] = True
        e2[vars[0]] = False

        partialProbSum1 = ithProbability1 * enumerateAll(bn, e1, vars[1:])
        partialProbSum2 = ithProbability2 * enumerateAll(bn, e2, vars[1:])

        return partialProbSum1+partialProbSum2

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

    distributionQ = enumerateAsk('B', {'J':True, 'M':True}, postOrderNodesCut, postOrderListCut)
    print(distributionQ)

main()