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

Steps to solve this problem:
    1. Iterate over each row in the list, where each row is a decode statement.
    2. Read the product line at the end of the decode statement
        IF a decode statement exists with the same product line AND has the same fields
            THEN concatenate the corresponding field values to the matching field, in ascending order
        ELSE create a new decode statement

Questions

Should I break it up into pieces, i.e. fields, and then return a series of strings?
Any ideas for selecting items? Use regex and -select
Use pprint for printing cleanly
"""
# Test data
decode1 = "IN((Product_Number)), '02') AND IN((Class_Code)), '4') AND IN((Type_Code)), '8','5') AND IN((Purpose_Code)), '530'),'Commercial'"
decode2 = "IN((Product_Number)), '06') AND IN((Class_Code)), '4') AND IN((Type_Code)), '1','3') AND IN((Purpose_Code)), '515', '530'),'Commercial'"

print(decode1)
