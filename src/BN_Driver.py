import test as xml
import Bayesian_Enumerator as ben
import sys

def main():
    # to get user input in order: fileName.xml query_variable evidence/truthValues
    print('****************************************************************')
    print('************ Welcome to the Bayesian Network Driver ************')
    print('****************************************************************')

    start = xml.bayesian_network('root')
    tree = xml.ET.parse('dog-problem.xml')  # right now this doesnt work for aima-wet-grass.xml
    root = tree.getroot()
    test = xml.make_nodes(root)
    networkList = xml.make_network(root, test, start)

    # topologically ordered list of nodes
    postOrderNodes = xml.linearize(networkList)
    postOrderNodesCut = postOrderNodes[1:]  # the entire list of nodes minus the root node

    # postOrderList is JUST A LIST OF NODE NAMES, NOT NODE OBJECTS
    postOrderList = xml.get_var_names(postOrderNodes)
    postOrderListCut = postOrderList[1:]  # the entire list of nodes minus the root node

    distributionQ = ben.enumerateAsk(['light-on', (True, False)], {'bowel-problem': False, 'hear-bark': True}, postOrderNodesCut, postOrderListCut)
    print('normalized Q value ', distributionQ)

if __name__ == '__main__':
    main()