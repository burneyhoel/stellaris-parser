'''
Created on 21 May 2016

@author: Ninetailed
'''

import os
from ninetailed.stellaris.techparser import TechParser

areacolors = {"engineering": "orange", "physics": "blue", "society": "green"}
stellarispath = "C:/Program Files (x86)/Steam/steamapps/common/Stellaris"

os.chdir(stellarispath)
os.chdir("common/technology")

print("graph {")
print("node [color=\"red\"]") # Use red to mark missing techs

parser = TechParser()
for filename in os.listdir():
    if len(filename) < 5 or filename[-4:] != ".txt":
        continue
    print("subgraph \"" + filename + "\" {")
    with open(filename, "r") as file:
        parsed = parser.parse(file.read())
        for key in parsed:
            value = parsed[key]
            if type(value) is not dict or "area" not in value:
                # This isn't a tech
                continue
            if value["area"] in areacolors:
                color = areacolors[value["area"]]
            else:
                color = "black"
            print(key + " [color=\"" + color + "\"]")
            if "prerequisites" in value:
                for prereq in value["prerequisites"].keys():
                    print(prereq + " -- " + key)
    print("}")
print("}")
