import xml_to_bn as xml
import Bayesian_Enumerator as ben
import sys
import bayesian_networks as qins

def main():
    # to get user input in order: fileName.xml query_variable evidence/truthValues
    print('\n')
    print('****************************************************************')
    print('************ Welcome to the Bayesian Network Driver ************')
    print('****************************************************************')
    print('\n')

    fileName = sys.argv[1]
    queryX = str(sys.argv[2])
    evidenceList = sys.argv[3:]

    evidenceE = {}
    for i in range(len(evidenceList)):
        if 'True' in evidenceList[i] or 'False' in evidenceList[i]: #if it's a letter/variable
            evidenceE[evidenceList[i-1]] = evidenceList[i]

    print('User entered values')
    print('File Selected : {}'.format(fileName))
    print('Query Variable : {}'.format(queryX))
    print('Evidence Provided : {}\n'.format(evidenceE))

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

    distributionQ = ben.enumerateAsk([queryX, ('True', 'False')], evidenceE, postOrderNodesCut, postOrderListCut)
    print('Results from Exact Inference :     ', distributionQ)
    
    l1 = []
    for k,v in evidenceE.items() :
        if v == 'True' and k != queryX:
            l1.append((k,1))
        if v == 'False' and k != queryX:
            l1.append((k,0))
    d = qins.rejection_sampling([(queryX , 1)] , l1, 10000 , postOrderNodes)
    c = qins.likelihood_sampling([(queryX , 1)] , l1, 10000 , postOrderNodes)
    print('Results from Likelihood Sampling : ' , [c , 1-c])
    print('Results from Rejection Sampling  : ' , [d , 1-d])
    if distributionQ[0] > c :
        error = ((distributionQ[0] - c)/(distributionQ[0])) * 100
    else:
        error = ((-distributionQ[0] + c)/(distributionQ[0])) * 100
    if distributionQ[0] > d :
        error1 = ((distributionQ[0] - d)/(distributionQ[0])) * 100
    else:
        error1 = ((-distributionQ[0] + d)/(distributionQ[0])) * 100
    print("Percentage difference between Exact Inference and Likelihood Sampling : " , error)
    print("Percentage difference between Exact Inference and Rejection Sampling  : " , error1)

if __name__ == '__main__':
    main()
