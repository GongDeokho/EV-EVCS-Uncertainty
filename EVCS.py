def pipeline(evcs,evcs_tot,evcs_plug,evcs_num,ev_day,time_slot):
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    
    #plug 개수랑 ev data랑 안맞으면 ev data 짤라야됨.
    if evcs_tot.size < len(ev_day):
        ev_day = ev_day.drop(range(evcs_tot.size,len(ev_day)))
        ev_day = ev_day.reset_index(drop = True)

    return [evcs,evcs_num,evcs_tot]

def evcs_after(evcs_tot,evcs_err,time_slot,ev_day,path):
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    import os
    
    err_num = []
    # evcs error 데이터 찾기
    for i in range(len(evcs_err)):
        if evcs_err['hardware_err'][i] == 1:
            err_num.append(i)
            for j in range(evcs_tot.shape[1]):
                if evcs_tot['#plug{}'.format(j)][i] == 1:
                    index = evcs_tot.index[evcs_tot['#plug{}'.format(j)] == 0]
                    if sum(index) != 0:
                        evcs_tot['#plug{}'.format(j)][index[0]] = 1
                        evcs_tot['#plug{}'.format(j)][i] = -1
                    else:
                        ev_day.iloc[i*5+j][['in','out']] = 0
            os.makedirs(path + '/result/EVCS/Day{}'.format(time_slot.day), exist_ok=True)
            evcs_tot.to_csv(path + '/result/EVCS/Day{}/evcs_h{}_m{}_errnum{}.csv'.format(time_slot.day,time_slot.hour,time_slot.minute,i))
                
    # recover time check & EVCS state update
    if sum(err_num) != 0:
        for i in range(len(err_num)):
            if evcs_err['evcs_recover_time'][i] == 0:
                evcs_tot.iloc[err_num[i]] = 0
    for i in range(evcs_tot.shape[0]-1):
        for j in range(evcs_tot.shape[1]):
            if (evcs_tot['#plug{}'.format(j)][i] == 0) & (evcs_tot['#plug{}'.format(j)][i+1] == 1):
                    evcs_tot['#plug{}'.format(j)][i] = 1
                    evcs_tot['#plug{}'.format(j)][i+1] = 0

    # recovery time counting
    if (sum(err_num) != 0) & (time_slot.minute == 0):
        for i in range(len(err_num)):
            evcs_err['evcs_recover_time'][i] = evcs_err['evcs_recover_time'][i] - 1

    return [evcs_err,ev_day,evcs_tot]