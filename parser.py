import xml.etree.ElementTree as ET
import sys
import re
from TreeNode import *

#rootNode = ""
previousParent = {}

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
                #print id, id.count("_")
                if count == 0:
                    previousId = id.count("_")
                    treeNode = TreeNode(id, id,"temp")
                    previousParent[previousId] = treeNode
                    rootNode = treeNode
                else :
                    currentIdLen = id.count("_")
                    if currentIdLen > previousId:
                        treeNode = TreeNode(id, id, "temp")
                        previousParent[currentIdLen] = treeNode
                        previousParent[previousId].children.append(treeNode)
                        previousId = currentIdLen
                    elif currentIdLen < previousId:
                        treeNode = TreeNode(id, id, "temp")
                        previousParent[currentIdLen] = treeNode
                        previousParent[currentIdLen - 1].children.append(treeNode)
                        previousId = currentIdLen
                    elif currentIdLen == previousId:
                        treeNode = TreeNode(id, id, "temp")
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
    print tabs, treeNode.id
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
