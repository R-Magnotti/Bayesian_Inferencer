import xml_to_bn as xml
import Bayesian_Enumerator as ben
import sys

def main():
    # to get user input in order: fileName.xml query_variable evidence/truthValues
    print('\n')
    print('****************************************************************')
    print('************ Welcome to the Bayesian Network Driver ************')
    print('****************************************************************')

    fileName = sys.argv[1]
    queryX = str(sys.argv[2])
    evidenceList = sys.argv[3:]

    evidenceE = {}
    for i in range(len(evidenceList)):
        if 'True' in evidenceList[i] or 'False' in evidenceList[i]: #if it's a letter/variable
            evidenceE[evidenceList[i-1]] = evidenceList[i]

    print('User entered values: ', fileName, queryX, evidenceList, evidenceE)

    start = xml.bayesian_network('root')
    #tree = xml.ET.parse('aima-alarm1.xml')
    tree = xml.ET.parse(fileName)
    root = tree.getroot()
    test = xml.make_nodes(root)
    networkList = xml.make_network(root, test, start)

    # topologically ordered list of nodes
    postOrderNodes = xml.linearize(networkList)
    postOrderNodesCut = postOrderNodes[1:]  # the entire list of nodes minus the root node

    # postOrderList is JUST A LIST OF NODE NAMES, NOT NODE OBJECTS
    postOrderList = xml.get_var_names(postOrderNodes)
    postOrderListCut = postOrderList[1:]  # the entire list of nodes minus the root node

    # distributionQ = ben.enumerateAsk(['B', (True, False)],
    #                                  {'J': True, 'M':True},
    #                                  postOrderNodesCut, postOrderListCut)

    distributionQ = ben.enumerateAsk([queryX, (True, False)], evidenceE,
                                     postOrderNodesCut, postOrderListCut)

    print('normalized distribution ', distributionQ)

if __name__ == '__main__':
    main()