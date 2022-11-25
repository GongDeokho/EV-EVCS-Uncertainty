import pandas as pd
import numpy as np
   
import Uncertainty
import EVCS
import EV
import Aggregator
ev_num = 1
input_path = './input/'

#ev parameter

#evcs parameter
#uncertainty parameter
err_rate = 20 #error rate
#time parameter
time_slot = 0
day = 0

while ev_num != 0:
    trigger = 0
    [ev,ev_day,tou,ev_num] = EV.pipeline(input_path,day,ev_num,trigger) # EV data 받아오기
    [evcs,evcs_num] = EVCS.pipeline(input_path,ev_day,trigger) # EVCS data
    [Power,trigger] = Aggregator.pipeline(ev_day,ev_num,evcs,evcs_plug,evcs_num,trigger,tou,day,time_slot) #Scheduling
    [evcs_err,ev_err] = Uncertainty.pipeline(input_path,err_rate,ev_day,evcs)
    time_slot = time_slot + 1
    if time_slot >= 23:
        time_slot = 0
        day = day + 1
    