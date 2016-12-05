""" Katie Lunceford
"""

import math

class Node:

    def __init__(self, data, values):
        self.data = data
        self.count = 0
        self.values = values
        self.children = [None]*len(values)

class DecisionTree:

    def __init__(self):
        self.root = None
        self.columns = None

    def train(self, data, inputAttr, maxDepth):
        self.columns = inputAttr
        self.root = makeTree(data, inputAttr, maxDepth)

    def evaluate(self, twoDList):
        return multiplePredictions(self.root, self.columns, twoDList)



def makeTree(data, inputAttr, maxDepth):
    if data == []:
        raise Exception
    state = True
    val = data[0][0]
    for x in range(len(data)):
        if data[x][0] != val:
            state = False
            break
    if state:
        n = Node(val, [])
        n.count = len(data)
        return n
    if len(inputAttr) == 1:
        items = []
        for x in range(len(data)):
            items.append(data[x][0])
        val = mostFreq(items)
        n = Node(val, [])
        n.count = len(data)
        return n
    ind = maxGain(data)
    keys = []
    for x in data:
        if not (x[ind] in keys):
            keys.append(x[ind])
    newNode = Node(inputAttr[ind],keys)
    newNode.count = len(data)
    for x in range(len(keys)):
        newData = []
        for y in data:
            if y[ind] == keys[x]:
                new = y[:ind] + y[ind+1:]
                newData.append(new)
        newInput = inputAttr[:ind] + inputAttr[ind+1:]
        newNode.children[x] = makeTree(newData, newInput, maxDepth)
    return newNode


def predict(root, columns, oneDList):
    if root == None:
        return None
    if root.children == []:
        return root.data
    ind = findIndex(root.data, columns)
    item = oneDList[ind]
    child = findIndex(item, root.values)
    if child == None:
        print('Cannot predict')
        return None
    answer = predict(root.children[child], columns, oneDList)
    return answer

def multiplePredictions(root, columns, twoDList):
    for x in twoDList:
        x[0] = predict(root, columns, x)
    return twoDList


def findIndex(val, l):
    for x in range(len(l)):
        if l[x] == val:
            return x
    return None





def mostFreq(items):
    dic = {}
    for i in range(len(items)):
        if items[i] in dic:
            dic[items[i]] += 1
        else:
            dic[items[i]] = 1
    maximum = max(dic, key=dic.get)
    return maximum

def maxGain(data):
    entropy = 2
    loc = 0
    for x in range(1,len(data[0])):
        items = []
        for y in range(len(data)):
            items.append([data[y][0],data[y][x]])
        ent = calculateEntropy(partition(items))
        if ent < entropy:
            entropy = ent
            loc = x
    return loc

def partition(twoDList):
    parts = []
    keys = []
    
    for x in range(len(twoDList)):
        if not (twoDList[x][1] in keys):
            keys.append(twoDList[x][1])
            
    for y in keys:
        l = []
        for x in range(len(twoDList)):
            if twoDList[x][1] == y:
                l.append(twoDList[x][0])
        parts.append(l)
    return parts

def calculateEntropy(partList):
    totEnt = 0
    totLen = 0
    for x in partList:
        totLen += len(x)
    for x in partList:
        ent = 0
        keys = []
        for y in x:
            if not (y in keys):
                keys.append(y)
        for key in keys:
            count = 0
            for y in x:
                if y == key:
                    count += 1
            length = len(x)
            val = -(count/length)* math.log(count/length,2)
            ent += val
        totEnt += (len(x)/totLen)*ent
    return totEnt


