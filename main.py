'''
Created on 24 February 2018

@author: Shamis
'''

import os
import sys
master_key_counter = 0
all_prereqs = ""
mod_name = "linear_trees"#need to make argument
from ninetailed.stellaris.techparser import TechParser
#C:\Python27\python.exe K:\git_repos\project_1\stellaris-parser\main.py F:/SteamLibrary/steamapps/common/Stellaris/common/technology
areacolors = {"engineering": "orange", "physics": "blue", "society": "green"}
stellarispath=sys.argv[1] if len(sys.argv) > 1 else "C:/Program Files (x86)/Steam/steamapps/common/Stellaris"
#stellarispath = "C:/Program Files (x86)/Steam/steamapps/common/Stellaris"
#stellarispath = "F:/SteamLibrary/steamapps/common/Stellaris"#need to pass as an argument
os.chdir(stellarispath)
#os.chdir("common/technology")

print("graph {")
print("node [color=\"red\"]") # Use red to mark missing techs

parser = TechParser()
Unwanted_tech_file = open("Unwanted_tech", "a")#starter tech and repeatables list
On_actions_file = open("On_actions", "a")#trigger list
On_actions_file.write("# A country has increased the level of a tech, use last_increased_tech trigger to check tech and level.\n")
On_actions_file.write("# This = Country\n")
On_actions_file.write("on_tech_increased = {\n")
On_actions_file.write("	events = {\n")
for filename in os.listdir(stellarispath):
    if len(filename) < 5 or filename[-4:] != ".txt":
        continue
    print("subgraph \"" + filename + "\" {")
    print(os.path.splitext(filename)[0])
    events_filename = ("events." + (os.path.splitext(filename)[0]))
    Events_file = open(events_filename, "a")#triggered scripts
    Events_file.write("namespace = " + mod_name + "\n")
    On_actions_file.write("		#" + events_filename + ".txt\n")
    with open(filename, "r") as file:
        parsed = parser.parse(file.read())
        for key in parsed:
            value = parsed[key]
            if type(value) is not dict or "area" not in value:
                # This isn't a tech
                continue
            if value["area"] in areacolors:
                color = areacolors[value["area"]]
                master_key_counter = master_key_counter + 1
                print(master_key_counter)
            else:
                color = "black"
                master_key_counter = master_key_counter + 1
                print(master_key_counter)
            print(key + " [color=\"" + color + "\"]")
            if "start_tech" in value:
                #we do not want this tech
                #all level 1 weapons are starter now
                #need to add techs with no prereq here
                #need at rare techs here
                #need to add repeatable techs here
                #need to add user requested techs here
                Unwanted_tech_file.write(key + " " + repr(master_key_counter) + " is a starter tech \n")
                continue
            if "prerequisites" in value:
                for prereq in value["prerequisites"].keys():
                    all_prereqs = (all_prereqs + " has_technology = \"" + prereq + "\"")
                else:
                    Events_file.write("country_event = {\n")
                    Events_file.write("  id = linear_trees." + repr(master_key_counter) + "\n")
                    Events_file.write("  hide_window = yes\n")
                    Events_file.write("  is_triggered_only = yes\n")
                    Events_file.write("  trigger = { is_ai = no " + all_prereqs + " }\n")
                    Events_file.write("  immediate = {\n")
                    Events_file.write("    if = {\n")
                    Events_file.write("      limit = {\n")
                    Events_file.write("        NOT = { has_tech_option = \"" + key + "\"" + " }\n")
                    Events_file.write("      }\n")
                    Events_file.write("      add_research_option = \"" + key  + "\"\n")
                    Events_file.write("    }\n")
                    Events_file.write("  }\n")
                    Events_file.write("}\n")
                    all_prereqs = ""
                    On_actions_file.write("		" + mod_name + "." + repr(master_key_counter) + " #" + key + "\n")
                    #need to make a list of starter and repeatable techs and use them to skip
    print("}")
On_actions_file.write("	}\n")
On_actions_file.write("}")
