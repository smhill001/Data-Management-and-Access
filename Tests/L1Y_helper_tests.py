# -*- coding: utf-8 -*-
"""
Created on Thu Sep 18 10:41:56 2025

@author: smhil
"""


#date string avg test
import process_L1Y_helpers as L1h

date1="2025-01-06T00:00:00"
date2="2025-01-06T06:00:00"
refresult="2025-01-06T03:00:00.000000"
result=L1h.averageDates(date1, date2, "%Y-%m-%dT%H:%M:%S.%f")

print(result)
print(refresult)

PF=(refresult==result)
print(PF)
