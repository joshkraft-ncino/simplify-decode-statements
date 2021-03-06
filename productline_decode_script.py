"""
The problem: decode statements in Informatica "Loan" MCT's are not concatenated properly - there are redundant lines that should be combined.
            This makes it difficult to troubleshoot Informatica errors, or add new products.

There are three decode statements of interest:
    - Product Line
    - Product
    - Product Type

Here is an example of a product line:

1. IN((Extract_Product_Number)), '21502') AND IN((Extract_Class_Code)), '4') AND IN((Extract_CollateralType_Code)), '38','35') AND IN((Extract_Purpose_Code)), '530'),'Commercial',
2. IN((Extract_Product_Number)), '21602') AND IN((Extract_Class_Code)), '4') AND IN((Extract_CollateralType_Code)), '1', '3') AND IN((Extract_Purpose_Code)),'514', '530'),'Commercial',
3. IN((Extract_Product_Number)), '21102') AND IN((Extract_Class_Code)), '5') AND IN((Extract_CollateralType_Code)), '20','21',) AND IN((Extract_Purpose_Code)), '518') AND IN((Extract_RE_Type_Code)), '202','203','204',),'Commercial',

In the above example, lines 1 and 2 should be combined, as they both contain the same fields and correspond to the same product line ('Commercial').
Line 3 should not be combined, as it contains an extra field which is not contained in Lines 1 or 2.

General To Do
    - Get list of numbers using regex, then sort ascending. Currently, regex selects a messy string
    - account for NA's (are all NA's using the same format? i.e. n/a, na, null, etc.)
    - Figure out sorting... dictionaries cannot be sorted. As such, access the sub dictionary
      and use the length of that, instead of total field length which depends on word length
    - Some statements point to multiple product lines?

Questions for Nicole:
    - Should product lines be sorted alphabetically?
    - Should I maintain sorting of fields within each statement?
    - Any for a tool to visualize nestings and for input of new codes?

"""

from pprint import pprint
import re

# Open file and grab decode line
file = open('productline_example.txt')
statements = file.readlines()
decodeLine = statements.pop(0)[0:-1]

# Create Master Combination dict (yet to be implemented)------------------------------
"""
masterDict = {}
for statement in statements:
    statement = statement[0:-1]
    productLine = statement.rsplit(sep=",'",maxsplit=1)[-1][0:-2]
    s1 = dict(statement.split(")") for item in statement.split("))"))
    print(s1)


    for k in masterDict.items():
        productLine = k

pprint(masterDict.items())
"""
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


    # Create string of concatenated field names - serves as unique ID for merging
    fieldsID = ''.join(fields)
    if fieldsID not in statementDict[productLine].keys():
        statementDict[productLine][fieldsID] = {}   # WHY is this blank?

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
        if f not in statementDict[productLine][fieldsID].keys():
            statementDict[productLine][fieldsID][f] = code

# Create decode statements -----------------------------------------------------
decodeList = []
for k, v in statementDict.items():
    productLine = k
    for k2, v2 in v.items():
        for k3, v3 in v2.items():
            field = k3
            values = v3

            string = f"IN(LTRIM(RTRIM({v2})), {values}), '{productLine}',\n"
            # TODO: Add formatting to match decode statement string. Make sure last line has no comma.
            decodeList.append(string)

decodeList.insert(0,decodeLine+'\n')
decodeString = ''.join(decodeList)
output =  open('output.txt','w')
output.write(decodeString)
output.close()


# Give user relevant section of decode -----------------------------------------------------
"""
Stage one: Get user input, suggest which line to look at for decode insertion
"""

line_input_string = input("What product type would you like to add: ")

if line_input_string in statementDict.keys():
    print("This product line already exists.")

    field_input_string = input("What fields would you like to add (comma separated)? ")
    field_input_list = [x.strip() for x in field_input_string.split(',')]
    field_input_concat = ''.join(field_input_list)

    if field_input_concat in statementDict[line_input_string].keys():

        print("This combination of fields already exists for this product line")
        print(statementDict[line_input_string][field_input_concat])

    else:
        print("This combination of field does NOT exist for this product line.")


else:
     print("That product line does not exist. Check your spelling!")
