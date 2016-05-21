# stellaris-parser
Tech tree parser for Stellaris

At present, this is just a Python script that reads in a tech file from a hardcoded path, and prints out a dot graph description (for use in Graphviz etc.) illustrating prerequisite relationships.

To do:
* Configurable Stellaris path rather than hard-coded
* Parse all tech files, not just one
* Load language files to give techs proper names
* (Maybe?) More information on tech bubbles, like area, tier, whether it's repeatable, etc.
