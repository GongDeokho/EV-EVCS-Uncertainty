def pipeline(input_path,day,ev_num,ev_count,hour):
    import pandas as pd
    import numpy as np
    
    ev = pd.read_csv(input_path+"evConfig.csv")
    
    if hour % 24 == 0: # day 마다 ev config 가져오기
        ev['init'] = ev['init'] * ev['cap'] # capacity 조정
        ev['target'] = ev['target'] * ev['cap']
        ev['min'] = ev['min'] * ev['cap']
        ev['max'] = ev['max'] * ev['cap']
        
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
        ev[['in','out','dur']] = ev[['in','out','dur']] * 60 # time-slot으로 조정
        
        ev_day = ev[(ev['Day'] == day) & (ev['ID'] <= ev_num-1)]
        ev_count = ev_count + ev_num
        
        # Cost
        tou = pd.read_csv(input_path+"tou.csv")
        
    return [ev,ev_day,tou,ev_num,ev_count]

def ev_after():
    test = 1
    return test