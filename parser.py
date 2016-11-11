import xml.etree.ElementTree as ET
import sys
import re
from TreeNode import *

#rootNode = ""
previousParent = {}

def getNodeType(line):
    match = re.search(':[rmog]* ',line)
    if match:
        type = match.group(0)
        if len(type) == 3:
            if type[1] == 'm':
                return "Mandatory"
            elif type[1] == 'g':
                return "Featured Group"
            elif type[1] == 'o':
                return "Optional"
            elif type[1] == 'r':
                return "Root"
        elif len(type) == 2:
            if type[1] == ' ':
                return "Group"
    else:
        raise Exception('Exception : Invalid Node Structure')


def getNodeName(line):
    pattern = re.compile(':[rmog]* ')
    match = pattern.split(line)[1]
    name = match[:match.index('(')]
    return name


def parseConstraints(structure):
    lines = structure.split("\n")
    for line in lines:
        line = line.strip()
        print line

def parseTree(structure):
    lines = structure.split("\n")
    rootNode = ""
    count = 0
    previousId = 0;
    for line in lines:
        if len(line) > 0:
            line = line.strip()
            match = re.search('\(.*\)',line)
            if match:
                id = match.group(0)[1:-1]
                nodeType = getNodeType(line)
                name = getNodeName(line)
                if len(name) == 0:
                    name = id
                #print id, id.count("_")
                if count == 0:
                    previousId = id.count("_")
                    treeNode = TreeNode(id, name, nodeType)
                    previousParent[previousId] = treeNode
                    rootNode = treeNode
                else :
                    currentIdLen = id.count("_")
                    if currentIdLen > previousId:
                        treeNode = TreeNode(id, name, nodeType)
                        previousParent[currentIdLen] = treeNode
                        previousParent[previousId].children.append(treeNode)
                        previousId = currentIdLen
                    elif currentIdLen < previousId:
                        treeNode = TreeNode(id, name, nodeType)
                        previousParent[currentIdLen] = treeNode
                        previousParent[currentIdLen - 1].children.append(treeNode)
                        previousId = currentIdLen
                    elif currentIdLen == previousId:
                        treeNode = TreeNode(id, name, nodeType)
                        previousParent[currentIdLen] = treeNode
                        previousParent[currentIdLen - 1].children.append(treeNode)
                        previousId = currentIdLen
                #print previousParent
                count += 1
            else:
                raise Exception('EXCEPTION: ID not present on Node')
    return rootNode

def dfsTree(treeNode, tabCount):
    tabs = "\t" * tabCount
    print tabs, treeNode.id , treeNode.name, "(" + treeNode.type + ")"
    for i in xrange(len(treeNode.children)):
        dfsTree(treeNode.children[i] ,tabCount+1)



assert len(sys.argv) == 2, "SPLOT Parser takes path to model.xml file as argument"

modelFile = sys.argv[1]
tree = ET.parse(modelFile)
root = tree.getroot()
rootNode = ""
for child in root:
    print child.tag, child.text
    if child.tag == "feature_tree":
        rootNode = parseTree(child.text);
    elif child.tag == "constraints":
        parseConstraints(child.text)
dfsTree(rootNode, 0)
