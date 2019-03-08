import re
# Example of numerical field values
v1 = '1'
v2 = '2'
v3 = '18'

listValues = []

# Append into one list, then run sort on that list
listValues.append(v1)
listValues.append(v3)
listValues.append(v2)

# Use key = int since I am running these numbers as STRINGS of NUMBERS
listValues.sort(key=int)

Values = ', '.join(listValues)

String = 'In nonsense ({}, {})'.format(Values, 'Hi')

print(String)

String2 = 'YEYEYEYEYEYEY, YEYEYEYEYEEY, hi'

String2 = String2.rsplit(',', 1)[1]

print(String2)

regex_fields = re.compile('/\(\(([^)]+)\)\)/')

String3 = '((hello))'

result = re.search(regex_fields, String3)

print(result.group())
