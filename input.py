def pipeline(path):
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    import os
    
    ############### time parameter
    
    time_slot = datetime(datetime.today().year,datetime.today().month,1,0,0)
    time = 48 #스케줄링 시간
    
    ############### EV
    
    ev = pd.read_csv(path+"/input/evConfig.csv")
    tou = pd.read_csv(path+"/input/tou.csv")
    
    # EV paramter
    ev_num = 30 # 일일 충방전 희망 차량 개수
    ev_count = 1 # 현재 충방전 중인 차량 개수
    ev_day = np.zeros([1,1]) #ev 사전할당용.
    ev_comp = np.zeros([1,1]) #스케줄 끝난 ev들 모으기
    
    # ev data 보정
    ev['init'] = ev['init'] * ev['cap'] # capacity 조정
    ev['target'] = ev['target'] * ev['cap']
    ev['min'] = ev['min'] * ev['cap']
    ev['max'] = ev['max'] * ev['cap']
    
    ############### EVCS
    evcs_plug = 5 # 충전소 1개 당 할당 EV 개수
    evcs = pd.read_csv(path + "/input/evcsConfig.csv")
    evcs_num = 11 # 충전소 개수. 걍 설정함.
    header = []

    for i in range(evcs_plug):
        header.append('#plug{}'.format(i))
    evcs_tot = pd.DataFrame(np.zeros([int(evcs_num),int(evcs_plug)]),columns = header)
    
    ############### Agg
    Power = pd.DataFrame(np.zeros([1,1])) #스케줄 모으기용
    Power_schedule = pd.DataFrame(np.zeros([1,1])) #충방전 끝난 EV들 스케줄 모으기
    
    
    ############### Uncertainty
    err_rate = 20 #error rate
    
    return [time_slot,time,tou,ev,ev_num,ev_count,ev_day,ev_comp,evcs_plug,evcs,evcs_num,evcs_tot,Power,Power_schedule,err_rate]