'''
Created on 10 May 2016

@author: Terrana
'''

import string
import re

class TechParser(object):
    '''
    classdocs
    '''
    ID_REGEX = re.compile("[a-zA-Z@_][a-zA-Z0-9@_]*")
    NUMBER_REGEX = re.compile("-?[0-9]+(\.[0-9]+)?")
    
    def __init__(self):
        '''
        Constructor
        '''
    
    def parse(self, work):
        ''' Main function. Parses the given work string into a dictionary of
        key-value pairs. '''
        pointer = 0
        length = len(work)
        result = dict()
        while (pointer < length):
            # Read the id of the next key
            pointer = self.skipWhitespaceAndComments(work, pointer);
            match = self.ID_REGEX.search(work, pointer)
            if (match == None):
                # No valid IDs left in file, so done
                break;
            key = match.group()
            pointer = match.end() + 1
            
            # Got a key, check for =
            pointer = self.skipWhitespaceAndComments(work, pointer)
            if (work[pointer] != '='):
                # No =, this isn't an assignment, record a value of None
                result[key] = None
                continue

            # This is an assignment, read the value
            pointer += 1
            value = self.readValue(work, pointer)
            pointer = value[1]
            result[key] = value[0]
        return result
    
    def skipWhitespaceAndComments(self, work, pointer):
        ''' Advances the pointer past any whitespace and/or comments. Returns the
        new pointer position. '''
        while(pointer < len(work) and string.whitespace.find(work[pointer]) > -1):
            pointer += 1
        if (pointer >= len(work)):
            return pointer
        
        if (work[pointer] == '/' or work [pointer] == '#'):
            comment = False
            if (work[pointer + 1] == '/' or work [pointer] == '#'):
                # Line comment
                commentEnd = "\n"
                comment = True
            elif (work[pointer + 1] == '*'):
                # Block comment
                commentEnd = "*/"
                comment = True
            
            if (comment):
                linebreak = work.find(commentEnd, pointer);
                if (linebreak != -1):
                    pointer = linebreak + 1
                    # Recurse to catch whitespace after comment
                    pointer = self.skipWhitespaceAndComments(work, pointer)
                else:
                    # End of file
                    pointer = len(work)
        return pointer
    
    def readValue(self, work, pointer):
        ''' Reads a value from the work string at the specified point, ignoring
        preceding whitespace, and returns a tuple of the read value, and the new
        pointer position.'''
        pointer = self.skipWhitespaceAndComments(work, pointer)
        nextChar = work[pointer]
        if (nextChar == '"'):
            # String
            endOfString = work.find('"', pointer + 1)
            result = work[pointer+1:endOfString]
            pointer = endOfString + 1
            return (result, pointer)
        elif (nextChar == '{'):
            # Table
            return self.parseTable(work, pointer)
        elif (self.ID_REGEX.match(work, pointer)):
            # Some identifier
            match = self.ID_REGEX.match(work, pointer)
            return (match.group(), match.end() + 1)
        elif (self.NUMBER_REGEX.match(work, pointer)):
            match = self.NUMBER_REGEX.match(work, pointer)
            return (match.group(), match.end() + 1)
        else:
            # Not a usable value
            while (string.whitespace.find(work[pointer]) == -1):
                pointer += 1
                if (pointer >= len(work)):
                    break
            return (None, pointer)
    
    def parseTable(self, work, pointer):
        ''' Reads a table value by finding the matching {}s and then recursively
        calling the main parser.'''
        pointer += 1  # skip past the initial {
        start = pointer
        length = len(work)
        bracketDepth = 1
        while (bracketDepth > 0 and pointer < length):
            nextChar = work[pointer]
            if (nextChar == '{'):
                bracketDepth += 1
            elif (nextChar == '}'):
                bracketDepth -= 1
            elif (string.whitespace.find(nextChar) != -1 or (nextChar == '/'
                         and (work[pointer+1] == '*' or work[pointer+1] == '/'))):
                pointer = self.skipWhitespaceAndComments(work, pointer)
                continue
            pointer += 1
        result = self.parse(work[start:pointer])
        pointer += 1
        return (result, pointer)
