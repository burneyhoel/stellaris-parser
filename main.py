'''
Created on 21 May 2016

@author: Ninetailed
'''

from ninetailed.stellaris.techparser import TechParser

file = open("C:/Program Files (x86)/Steam/steamapps/common/Stellaris/common/technology/00_eng_tech.txt", "r")
inputStr = file.read()
parser = TechParser()
parsed = parser.parse(inputStr)
print("graph {")
print("node [color=\"red\"]") # Use red to mark missing techs
for key in parsed:
    value = parsed[key]
    if type(value) is not dict:
        continue
    print(key + " [color=\"black\"]")
    if "prerequisites" in value:
        for prereq in value["prerequisites"].keys():
            print(prereq + " -- " + key)
print("}")
