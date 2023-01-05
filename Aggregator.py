def pipeline(ev_day,ev_num,ev_count,evcs,evcs_plug,evcs_num,evcs_tot,tou,time_slot,time):
    import pandas as pd
    import gurobipy as gp
    import numpy as np
    from gurobipy import GRB
    from datetime import datetime, timedelta
         
    # target SoC >> power * Pmax 부분 조정하기 --> Dumb charge로
    for i in range(len(ev_day)):
        if ev_day['target'][i] >= evcs['Pmax'][i+((time_slot.day-1)*len(ev_day))] * ev_day['dur'][i]:
            ev_day['target'][i] = evcs['Pmax'][i+((time_slot.day-1)*len(ev_day))] * ev_day['dur'][i]
            
    # ## 모델 선언
    Power = 0
    # m = gp.Model("Aggregator")
    
    # ## 변수 선언 : 효율 때문에 충방전 나눔.
    # Power_pos = [m.addVars(range(ev_day['dur'][vdx]), ub=evcs['Pmax'][vdx+(day*len(ev_day))], lb= 0, vtype = GRB.INTEGER) for vdx in range(len(ev_day))]
    # Power_neg = [m.addVars(range(ev_day['dur'][vdx]), ub= 0, lb=evcs['Pmin'][vdx+(day*len(ev_day))], vtype = GRB.INTEGER) for vdx in range(len(ev_day))]
    # U = [m.addVars(range(ev_day['dur'][vdx]), vtype = GRB.BINARY) for vdx in range(len(ev_day))]
    
    # for idx in range(len(ev_day)):
    #     SOC = ev_day['init'][idx]
    #     for t in range(ev_day['dur'][idx]):
    #         ## Constraint 1 : 충방전 동시에 되지 않게 하기
    #         m.addConstr(Power_pos[idx][t] <= U[idx][t] * evcs['Pmax'][idx])
    #         m.addConstr(Power_neg[idx][t] >= (1-U[idx][t]) * evcs['Pmin'][idx])
            
    #         ## Constraint 2 : SoC boundary
    #         SOC += Power_pos[idx][t] * ev_day['chg_eff'][idx]/100 + Power_neg[idx][t] * ev_day['dchg_eff'][idx]/100
    #         m.addConstr(SOC >= ev_day['min'][idx])
    #         m.addConstr(SOC <= ev_day['max'][idx])
            
    #     ## Cosntraint 3 : Target SoC
    #     m.addConstr(SOC >= ev_day['target'][idx])
        
    # ## 목적함수: 시간별 에너지 비용(전력량요금) (최소화)
    # obj1 = gp.quicksum(Power_pos[idx][t] * tou['ToU'][ev_day['in'][idx]+t] + Power_neg[idx][t] * tou['ToU'][ev_day['in'][idx]+t] for idx in range(len(ev_day)) for t in range(ev_day['dur'][idx]))
        
    # m.setObjective(obj1, GRB.MINIMIZE)
    # m.optimize()
    # # 결과 정리
    # Power = pd.DataFrame(np.zeros([len(ev_day),time]))

    # # 스케줄 저장하기
    # for idx in range(len(ev_day)):
    #     for t in range(ev_day['dur'][idx]):
    #         Power[idx][ev_day['in'][idx]-1 + t] = Power_pos[idx][t].X + Power_neg[idx][t].X
    
    #충전소에 EV들 할당하기
    park_num = len(ev_day)
    for i in range(int(evcs_num)):
        for j in range(int(evcs_plug)):
            if (evcs_tot['#plug{}'.format(j)][i] == 0) & (park_num != 0):
                evcs_tot['#plug{}'.format(j)][i] = 1
                park_num = park_num - 1

    ev_count = sum(evcs_tot[evcs_tot==1].count())
    return [Power,evcs_tot,ev_count]