def pipeline(ev,ev_num,ev_count,time_slot,ev_day,ev_comp,tou):
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    import os
     
    # EV target SoC 조정
    for vdx in range(len(ev)):
        if ev['out'][vdx] < ev['in'][vdx]:
            ev['out'][vdx] += 24
    for vdx in range(len(ev)):
        if ev['init'][vdx] >= ev['target'][vdx]:
            ev['init'][vdx] = ev['target'][vdx]/2
            
    # EV plug-out time 오버되는거 조정
    for vdx in range(len(ev)):
        if ev['out'][vdx] > 47:
            ev['out'][vdx] = 47
    ev['dur'] = ev['out'] - ev['in'] 
    
    # ev data 가져오기
    if ev_day.sum().sum()== 0:
        ev_day = ev[(ev['Day'] == time_slot.day - 1) & (ev['ID'] <= ev_num-1)]
    
    # day에 맞춰서 index 추가하기
    if (time_slot.day != 1) & (time_slot.hour == 0) & (time_slot.minute == 0):
        ev_day = ev_day.append(ev[ev['Day'] == time_slot.day - 1],ignore_index = True)
        ev_day = ev_day.reset_index(drop = True)

    
    # EV data update
    for i in range(len(ev_day)):
        # time update at every hour
        if ev_day.sum().sum() == 0:
            ev_day[['in','out','dur']][i] = ev_day[['in','out','dur']][i] - 1
        
        # time update at next day
        if (ev[ev == ev_day.loc[i]].dropna()['out']).empty == 0:
            if int(ev[ev == ev_day.loc[i]].dropna()['out']) > 24:
                if (ev_day['Day'][i] == time_slot.day) & (time_slot.hour):
                    ev_day[['in','out','dur']][i] = ev_day[['in','out','dur']][i] - 1
                
    # EV data minus
        if ev_day['in'][i] <= 0:
            ev_day['in'][i] = 0
            
    # complete EV data
        if ev_day['out'][i] <= 0:
            if ev_comp.sum() == 0:
                ev_comp = ev_day.loc[i]
            else:
                ev_comp = ev_comp.append(ev_day.loc[i])
            ev_day = ev_day.drop(i)
            
    # index reset
    ev_day = ev_day.reset_index(drop=True)
   
    return [ev,ev_day,tou,ev_num,ev_count,ev_comp]

# def ev_after(path,ev_num,ev_count,time_slot,ev_day,ev_comp):