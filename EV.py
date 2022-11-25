def pipeline(input_path,day,ev_num,trigger):
    import pandas as pd
    import numpy as np
    
    if trigger == 0:
        ev = pd.read_csv(input_path+"evConfig.csv")
        ev['init'] = ev['init'] * ev['cap']
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
        ev_day = ev[(ev['Day'] == day) & (ev['ID'] <= ev_num)]
        
        # Cost
        tou = pd.read_csv(input_path+"tou.csv")
    else:
        test = 1
    
    return [ev,ev_day,tou,ev_num]