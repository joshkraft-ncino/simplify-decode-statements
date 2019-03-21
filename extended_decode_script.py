from pprint import pprint
import re

"""
General To Do
    - Get list of numbers using regex, then sort ascending
    - account for NA's (are all NA's using the same format?)
    - Figure out sorting... dictionaries cannot be sorted. As such, access the sub dictionary
      and using the length of that, instead of total field length which depends on word length
    - Some statements point to multiple product lines?
    - Sort product lines alphabetically?
"""



# Open file and grab decode line
file = open('productline_example.txt')
statements = file.readlines()
decodeLine = statements.pop(0)[0:-1]

# Create template --------------------------------------------------------------
statementDict = {}
for statement in statements:
    statement = statement[0:-1]
    # Get product line of statement
    productLine = statement.rsplit(sep=",'",maxsplit=1)[-1][0:-2]
    # If not in dict, add it
    if productLine not in statementDict.keys():
        statementDict[productLine] = {}
    # Get fields of statement
    fieldRegex = re.compile(r'RTRIM\((.*?)\)')
    fields = re.findall(fieldRegex,statement)
    fields.sort() #WHY are fields sorted here alphabetically? I think the order matters.
    # Create string of concatenated field names - serves as unique ID for merging
    fieldsID = ''.join(fields)
    if fieldsID not in statementDict[productLine].keys():
        statementDict[productLine][fieldsID] = {}   # WHY is this blank?
    for f in fields:
        string = f+'numbers'
        # TODO: get sorted list of numbers and replace string var. Need to write regex that selects numbers
        # May use AND statement as a reference... but, need to account for last group of numbers
        if f not in statementDict[productLine][fieldsID].keys():
            statementDict[productLine][fieldsID][f] = string

# Create decode statements -----------------------------------------------------
decodeList = []
for k, v in statementDict.items():
    productLine = k
    for k2, v2 in v.items():
        for k3, v3 in v2.items():
            field = k3
            values = v3

            string = f'{productLine}, {field}, {values}\n'
            # TODO: Add formatting to match decode statement string
            decodeList.append(string)

decodeList.insert(0,decodeLine+'\n')
decodeString = ''.join(decodeList)
output =  open('output.txt','w')
output.write(decodeString)
output.close()
pprint(statementDict)
