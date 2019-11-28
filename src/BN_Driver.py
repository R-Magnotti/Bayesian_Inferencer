import xml_to_bn as xml
import Bayesian_Enumerator as ben
import sys

def main():
    # to get user input in order: fileName.xml query_variable evidence/truthValues
    print('****************************************************************')
    print('************ Welcome to the Bayesian Network Driver ************')
    print('****************************************************************')
    correct = 'N'
    while correct == 'N':
        try:
            fileName = input('\nWhich file would you like to access?\n')
        
        queryX = input('\nPlease enter the query variable: \n')
        evidenceE = {}

        n = input('\nPlease enter the number of total evidence variables: \n')
        for i in range(int(n)):
            print('\nWhat is the ', i + 1, 'th variable name?')
            var = input('')
            print('\nWhat is ', var, "'s truth value?")
            tValue = input('')
            evidenceE[var] = bool(tValue)

        print('\n')
        print('You have entered:\n', 'File name: ', fileName, '\nQuery: ', queryX, '\nEvidence: ', evidenceE, )
        correct = input('\nIs this correct? Y/N\n')

    print('----------------------CALCULATIONS----------------------')

    start = xml.bayesian_network('root')
    #tree = xml.ET.parse('aima-alarm1.xml')  # right now this doesnt work for aima-wet-grass.xml
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

    print('normalized Q value ', distributionQ)

if __name__ == '__main__':
    main()