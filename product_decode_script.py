from pprint import pprint
import re
import csv

# Open file and grab decode line
file = open('simple_aff_product_example.txt')
statements = file.readlines()
decodeLine = statements.pop(0)[0:-1]

# Create dicitonary of values --------------------------------------------------------------
statementDict = {}
statementDF = []

for statement in statements:
    statement = statement[0:-1]
    products = []
    fields = []

    # Get product of statement
    product = statement.rsplit(sep=",'",maxsplit=1)[-1][0:-3]
    # If not in dict, add it
    if product not in statementDict.keys():
        statementDict[product] = {}
        products.append(product)

    # Get fields of statement
    fieldRegex = re.compile(r'RTRIM\((.*?)\)')
    fields = re.findall(fieldRegex,statement)


    # Create string of concatenated field names - serves as unique ID for merging
    fieldsID = ''.join(fields)
    if fieldsID not in statementDict[product].keys():
        statementDict[product][fieldsID] = {}   # WHY is this blank?

    # Get numbers + sort
    for f in fields:
        # TODO: Clean up regex. This is a messy workaround
        codeRegex = re.compile("(?<=%s\)\)\, )'(.*?)'(?=\))" % f)
        code = re.findall(codeRegex,statement)
        #code = [c.replace("'",'').split(',') for c in code][0]
        #code = [int(c) for c in code if c != 'N/A']
        #code.sort()
        #Conver code to string here?
        # TODO: get sorted list of numbers and replace string var. Need to write regex that selects numbers
        if f not in statementDict[product][fieldsID].keys():
            statementDict[product][fieldsID][f] = code
        print(products)
        print(fields)
        print(f)


# Output CSV for viewing/editing product decode statements ---------------------



# Convert CSV back into decode statement for input into Informatica ------------
