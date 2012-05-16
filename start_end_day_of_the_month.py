# -*- coding:utf-8 -*-
"""
Created on 25 jul 2011

@author: Administrator
"""

from datetime import date, timedelta
import re

def get_first_day(dt, d_years=0, d_months=0):
    # d_years, d_months are "deltas" to apply to dt
    y, m = dt.year + d_years, dt.month + d_months
    a, m = divmod(m-1, 12)
    return date(y+a, m+1, 1)

def get_last_day(dt):
    return get_first_day(dt, 0, 1) + timedelta(-1)

def start_end_day_of_the_month(year, month):

    h = str(get_first_day(date(year,month,1)))
    list = re.split('-',h)
    list_int = [int(x) for x in list]

    i = str(get_last_day(date(year,month,1)))
    list2 = re.split('-',i)
    list_int2 = [int(x) for x in list2]

    return [list_int[2], list_int2[2]]
