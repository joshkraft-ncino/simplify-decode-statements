"""
The problem: decode statements in Informatica "Loan" MCT's are not concatenated properly - there are redundant lines that should be combined.
            This makes it difficult to troubleshoot Informatica errors, or add new products.

There are three decode statements of interest:
    - Product Line
    - Product
    - Product Type

IN((Extract_Product_Number)), '21502') AND IN((Extract_Class_Code)), '4') AND IN((Extract_CollateralType_Code)), '38','35') AND IN((Extract_Purpose_Code)), '530'),'Commercial',
IN((Extract_Product_Number)), '21602') AND IN((Extract_Class_Code)), '4') AND IN((Extract_CollateralType_Code)), '0') AND IN((Extract_Purpose_Code)),'514', '530'),'Commercial',
"""
import pandas as pd
