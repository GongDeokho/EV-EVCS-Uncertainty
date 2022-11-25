def pipeline(input_path,ev_day,trigger,evcs_plug):
    import pandas as pd
    import numpy as np
    if trigger == 0:
        evcs = pd.read_csv(input_path + "evcsConfig.csv")
        evcs_num = np.ceil(len(ev_day) / 2.8) # 2021년 전기차 & 충전소 비율 : 2.8:1
        header = []
        for i in range(evcs_plug):
            header.append('#plug{}'.format(i))
        evcs_tot = pd.DataFrame(np.zeros([int(evcs_num),int(evcs_plug)]),columns = header)
    else:
        test = 1
    return [evcs,evcs_num,evcs_tot]