import xml.etree.ElementTree as ET
import random

class bayesian_network:

  def __init__(self , name):
    self.name = name
    self.children = []
    self.parent = []
    self.probs = None
    self.value = 0

  def __repr__(self):
    one = ("Variable Name : {}\n".format(self.name))
    two = ("Number of children : {}\n".format(len(self.children)))
    three = ("Number of parents : {}\n".format(len(self.parent)))
    four = ("Value : {}\n".format(self.value))
    return one + two + three + four

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
      print("Bro , your XML file is not in the format Jeet would approve of ~")
  
  return var_nodes


def find_corresponding_node(var_nodes , name):
  for i in var_nodes:
    if i.name == name:
      break
  return i

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

def space_parser(text):
  text = text + "  "
  l1 = []
  j = 0
  for i in range(len(text)):
    if text[i] == " ":
      print(text[j:i])
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
      print("Bro , your XML file is not in the format Jeet would approve of ~")
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


class queue:

  def __init__(self):
    self.state = []

  def add(self , element):
    if element not in self.state:
      self.state.append(element)
  
  def get(self):
    x = self.state[0]
    del self.state[0]
    return x

def check_if_condition_satisfied(network , list_var):
  count = 0
  for k,v in list_var:
    if find_corresponding_node(network , k).value == v:
      count = count + 1
  if count == len(list_var):
    return True
  else:
    return False

def flip(node):
  if node.parent[0].name == 'root':
    node.flip(node.probs[0])
  else:
    value = [1]
    for i in node.parent:
      value.append(i.value)
    binary = 0
    for i in range(len(value)):
      binary = binary + (2**(len(value)- 1 - i))*value[i]
    number = len(node.probs) - 1 - binary
    node.flip(node.probs[number])

def rejection_sampling(query_vars , evidence_vars , number_of_runs , network):
  count = 0
  event_count = 0
  number = 0
  while count < number_of_runs:
    number = number + 1
    q = queue()
    q.add(network[0])
    while q.state != []:
      u = q.get()
      for i in u.children:
        q.add(i)
      if u.name == 'root':
        continue
      flip(u)
    if check_if_condition_satisfied(network , evidence_vars):
      count = count + 1
      if check_if_condition_satisfied(network , query_vars):
        event_count = event_count + 1
  print(event_count/count , number)

def probability(a):
  l1 = [a.value]
  for i in a.parent:
    l1.append(i.value)
  binary = 0
  for i in range(len(l1)):
    binary = binary + (2**(len(l1)- 1 - i))*l1[i]
  number = len(a.probs) - 1 - binary
  return a.probs[number]

def likelihood_sampling(query_vars , evidence_vars , number_of_runs , network):
  count = 0
  event_count = 0
  number = 0
  while number < number_of_runs:
    weight = 1
    q = queue()
    q.add(network[0])
    while q.state != []:
      u = q.get()
      for i in u.children:
        q.add(i)
      if u.name == 'root':
        continue
      flag = 0
      for k,v in evidence_vars:
        if u.name == k:
          u.value = v
          weight = weight * probability(u)
          flag = 1
      if flag == 0:
        flip(u)
    count = count + weight
    number = number + 1
    if check_if_condition_satisfied(network , query_vars):
      event_count = event_count + weight
  return (event_count/count)

#rejection_sampling([('dog-out' , 1)] , [('family-out' , 0) , ('light-on' , 1)] , 20000 , y)

#likelihood_sampling([('family-out' , 1)] , [('dog-out' , 1) , ('bowel-problem' , 0) , ('hear-bark' , 1)] , 2000000 , y)

