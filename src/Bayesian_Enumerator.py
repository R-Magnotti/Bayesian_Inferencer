import xml_to_bn as xml
#from xml_to_bn import

#params:
#   X = query X. 1 symbol: str/char
#   evidence = as many variables as are provided as initial evidence. i number of symbols: dict
#   bn = bayesian network, represented by unordered list
#   varList = list of variables in topological order
def enumerateAsk(X, evidence, bn, varList):
    #Q is the distribution which in our case will only have 1 element
    Q = None #will be a single float value
    # would be a forloop if we didn't have the prerequisite that the query can only be one variable
    evidence.append(X)

    print(varList)

    Q = enumerateAll(bn, evidence, varList)

#takes params list representation of bayesian network bn, and evidence e
def enumerateAll(bn, e, vars):
    if

# global scope variables from the xml parser
def main():
    start = xml.bayesian_network('root')
    tree = xml.ET.parse('aima-alarm1.xml')
    root = tree.getroot()
    test = xml.make_nodes(root)
    networkList = xml.make_network(root, test, start)

    # topologically ordered list of nodes
    # y[0] is the root node of the graph which represents the entire graph
    postOrderNodes = xml.linearize(networkList)

    postOrderList = xml.get_var_names(postOrderNodes)
    print(postOrderList)

    enumerateAsk('A', ['B', 'C'], networkList, postOrderList)

main()