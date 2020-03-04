#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-02-07 10:28
# @Author  : July
import pandas as pd


data = pd.date_range(start='20200223', end='20200301')
date_list = data.array
date_lists = []
for i in date_list:
    date_lists.append(str(i)[0:10])
print(date_lists)


# for i in range(10, 20):
#     print(i)
#     for j in range(0, 9):
#         print(j)
#         if j == 3:
#             break