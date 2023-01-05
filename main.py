import pandas as pd
import numpy as np
from datetime import datetime, timedelta
   
import Uncertainty
import EVCS
import EV
import Aggregator
ev_num = 1
input_path = './input/'

#ev parameter
ev_num = 30 # 일일 충방전 희망 차량 개수
ev_count = 1 # 현재 충방전 중인 차량 개수

#evcs parameter
evcs_plug = 5 # 충전소 1개 당 할당 EV 개수

#uncertainty parameter
err_rate = 20 #error rate

#time parameter
time_slot = datetime(datetime.today().year,datetime.today().month,1,0,0)
time = 48 #스케줄링 시간

while True:
    ev_count = 0
    #Scheduling
    [ev,ev_day,tou,ev_num,ev_count] = EV.pipeline(input_path,ev_num,ev_count,time_slot) # EV data 받아오기
    [evcs,evcs_num,evcs_tot] = EVCS.pipeline(input_path,ev_day,evcs_plug,time_slot) # EVCS data
    
    # 매 시간마다 스케줄링 진행
    if time_slot.minute == 0:
        [Power,evcs_tot,ev_count] = Aggregator.pipeline(ev_day,ev_num,ev_count,evcs,evcs_plug,evcs_num,evcs_tot,tou,time_slot,time) #Scheduling
    
    [evcs_err,ev_err] = Uncertainty.pipeline(err_rate,ev_day,ev_num,evcs,evcs_num,evcs_plug)
    
    #Uncertainty 적용
    [evcs_err,ev_err,evcs_tot] = EVCS.evcs_after(evcs_tot,evcs_err,time_slot,ev_day)
    
    #time slot update
    time_slot = time_slot + timedelta(minutes = 1)
    
    if time_slot.day == 3:
        break
print(time_slot)