import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
   
import Uncertainty
import EVCS
import EV
import Aggregator
import input
ev_num = 1
path = os.path.abspath("C:\\Users\\PSSENL\\OneDrive - 경북대학교\\바탕 화면\\대학원\\EMS\\코딩\\8. EVCS & Uncertainty & EV")

[time_slot,time,tou,ev,ev_num,ev_count,ev_day,ev_comp,evcs_plug,evcs,evcs_num,evcs_tot,Power,Power_schedule,err_rate] = input.pipeline(path)

while True:
    ev_count = 0
    
    #uncertainty
    [evcs_err,ev_err] = Uncertainty.pipeline(err_rate,ev,ev_num,evcs,evcs_num,evcs_plug)   
    
    #Scheduling
    [ev,ev_day,tou,ev_num,ev_count,ev_comp] = EV.pipeline(ev,ev_num,ev_count,time_slot,ev_day,ev_comp,tou) # EV data 받아오기
    [evcs,evcs_num,evcs_tot] = EVCS.pipeline(evcs,evcs_tot,evcs_plug,evcs_num,ev_day,time_slot) # EVCS data
    
    # 매 시간마다 스케줄링 진행
    if time_slot.minute == 0:
        [Power,evcs_tot,ev_count] = Aggregator.pipeline(ev_day,ev_num,ev_count,evcs,evcs_plug,evcs_num,evcs_tot,tou,time_slot,time,path) #Scheduling
    
    #Uncertainty 적용
    [evcs_err,ev_err,evcs_tot] = EVCS.evcs_after(evcs_tot,evcs_err,time_slot,ev_day,path)
    # [evcs_err,ev_err,evcs_tot] = EV.ev_after(evcs_tot,evcs_err,time_slot,ev_day)
    
    #time slot update
    time_slot = time_slot + timedelta(minutes = 1)
    
    if time_slot.day == 3:
        break
print(time_slot)