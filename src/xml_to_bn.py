import xml.etree.ElementTree as ET
import random

class Queue:
  def __init__(self):
    self.queue = []

  def enqueue(self, value):
    self.queue.append(value)

  def dequeue(self):
    return self.queue.pop(0)

  def isEmpty(self):
    return self.queue == []

class bayesian_network:

  def __init__(self , name):
    self.name = name
    self.children = []
    self.parent = []
    self.probs = None
    self.value = 0

  # def __repr__(self):
  #   one = ("Variable Name : {}\n".format(self.name))
  #   two = ("Number of children : {}\n".format(len(self.children)))
  #   three = ("Number of parents : {}\n".format(len(self.parent)))
  #   four = ("Value : {}\n".format(self.value))
  #   return one + two + three + four

  def flip(self , p):
    if random.random() < p :
      self.value = 1
    else:
      self.value = 0

def make_nodes(xml_node):

  l1 = []
  var_nodes = []
  for i in xml_node.iter('VARIABLE'):
    l1.append(i)
  for var in l1:
    if var[0].tag == 'NAME':
      var_nodes.append(bayesian_network(var[0].text))
    else:
      print("The XML file does not have the tag <NAME> as its first field , please reformat it")
  
  return var_nodes

def remove_white_spaces(text):
  l1 = []
  l2 = []
  for i in range(len(text)):
    if text[i] == " ":
      l1.append(i)
  if l1 == []:
    return text
  for i in range(len(l1) - 1):
    count = l1[i]
    count = count + 1
    while count < l1[i+1]:
      l2.append(count)
      count = count + 1
  new_string = ''
  if l2 == []:
    return 5
  for i in l2:
    new_string = new_string + text[i]
  return new_string

def find_corresponding_node(var_nodes , name):
  for i in var_nodes:
    if i.name == name:
      break
  return i

def space_parser(text):
  text = text + "  "
  l1 = []
  j = 0
  for i in range(len(text)):
    if text[i] == " ":
      if remove_white_spaces(" " + text[j:i] + " ") != 5:
        l1.append(float(remove_white_spaces(" " + text[j:i] + " ")))
        j = i+1
  return l1

def make_network(xml_node , var_nodes , root_node):

  l1 = []
  for i in xml_node.iter('DEFINITION'):
    l1.append(i)
  for i in l1:
    if not ((i[0].tag == 'FOR') and (i[len(i) - 1].tag == 'TABLE')):
      print("The XML file does not have either the first tag as <FOR> or does not have the last tag as <TABLE>, please reformat it")
    else:
      if len(i) == 2:
        t = find_corresponding_node(var_nodes , i[0].text)
        t.parent.append(root_node)
        root_node.children.append(t)
        t.probs = space_parser(i[1].text)
      else:
        t = find_corresponding_node(var_nodes , i[0].text)
        for kk in range(1,len(i) - 1):
          t1 = find_corresponding_node(var_nodes , i[kk].text)
          t1.children.append(t)
          t.parent.append(t1)
        t.probs = space_parser(i[len(i) - 1].text)
  return [root_node] + var_nodes

def get_var_names(y):
  l1 = []
  for i in y:
    l1.append(i.name)
  return l1

#this function linearizes the order of nodes based on their dependencies and returns the topological ordering
#accepts root node n, and bn - Baye Network as list
def linearize(bn):
  #n = root node
  n = bn[0]
  postOrderNetworkList = []
  visited = {}
  #zero out the list of visited nodes
  for item in bn:
    visited[item.name] = False

  Q = Queue()

  Q.enqueue(n)
  visited[n.name] = True

  while Q.isEmpty() is False:
    n = Q.dequeue()
    postOrderNetworkList.append(n)

    for item in n.children:
      if visited[item.name] == False:
        Q.enqueue(item)
        visited[item.name] = True

  return postOrderNetworkList
