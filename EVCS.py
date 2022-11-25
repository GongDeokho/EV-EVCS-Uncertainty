def pipeline(input_path,ev_day,trigger):
    import pandas as pd
    import numpy as np
    if trigger == 0:
        evcs = pd.read_csv(input_path + "evcsConfig.csv")
        evcs_num = np.ceil(len(ev_day) / 2.8) # 2021년 전기차 & 충전소 비율 : 2.8:1
    else:
        test = 1
    return [evcs,evcs_num]