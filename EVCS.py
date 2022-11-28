def pipeline(input_path,ev_day,evcs_plug):
    import pandas as pd
    import numpy as np
    
    evcs = pd.read_csv(input_path + "evcsConfig.csv")
    evcs_num = np.ceil(len(ev_day) / 2.8) # 2021년 전기차 & 충전소 비율 : 2.8:1
    evcs_num = int(evcs_num)
    header = []
    for i in range(evcs_plug):
        header.append('#plug{}'.format(i))
    evcs_tot = pd.DataFrame(np.zeros([int(evcs_num),int(evcs_plug)]),columns = header)        
    return [evcs,evcs_num,evcs_tot]

def evcs_after(evcs_tot,evcs_err,Power,evcs_num,evcs_plug,time_slot):
    import pandas as pd
    import numpy as np
    plug_in = np.zeros([1,evcs_plug])
    index_error = []
    
    # plug
    for i in range(evcs_plug):
        plug_in[0][i] = len(evcs_tot['#plug{}'.format(i)][evcs_tot['#plug{}'.format(i)] == 1])
    for i in range(evcs_num):
        for j in range(evcs_plug):
            if (evcs_err['hardware_err'][i] == 1):
                evcs_tot['#plug{}'.format(j)][plug_in[0][j]] = 1
                evcs_tot['#plug{}'.format(j)][i] = None
                index_error = index_error.append(i)
    for i in range(evcs_plug):
        if (pd.isna(evcs_tot['#plug{}'.format(i)]) == 1) & (time_slot == evcs_err['evcs_recover_time'][pd.isna(evcs_tot['#plug{}'.format(i)])]):
            evcs_tot['#plug{}'.format(i)][pd.isna(evcs_tot['#plug{}'.format(i)])] = 0
    return test