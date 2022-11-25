import pandas as pd
import numpy as np
   
import Uncertainty
import EVCS
import EV
import Aggregator
input_path = './input/'

#ev parameter
ev_num = 30 # 일일 충방전 희망 차량 개수
#evcs parameter
evcs_plug = 5 # 충전소 1개 당 할당 EV 개수
#uncertainty parameter
err_rate = 20 #error rate
#time parameter
time = 48 #스케줄링 시간
day = 0

while ev_num != 0:
    trigger = 0
    [ev,ev_day,tou,ev_num] = EV.pipeline(input_path,day,ev_num,trigger) # EV data 받아오기
    [evcs,evcs_num,evcs_tot] = EVCS.pipeline(input_path,ev_day,trigger,evcs_plug) # EVCS data
    [Power,trigger] = Aggregator.pipeline(ev_day,ev_num,evcs,evcs_plug,evcs_num,trigger,tou,day,time_slot) #Scheduling
    [evcs_err,ev_err] = Uncertainty.pipeline(input_path,err_rate,ev_day,evcs)
    time_slot = time_slot + 1
    if time_slot >= time*60-1:
        time_slot = 0
        day = day + 1
    