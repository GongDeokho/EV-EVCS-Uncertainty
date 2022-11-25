def pipeline(ev_day,ev_num,ev_count,evcs,evcs_plug,evcs_num,evcs_tot,trigger,tou,day,time_slot,time):
    import pandas as pd
    import gurobipy as gp
    import numpy as np
    from gurobipy import GRB

    obj1 = 0
    # 충전기 개수만큼 ev 준비
    if ev_num >= evcs_plug * evcs_num:
        ev_day = ev_day[ev_day['ID'] <= evcs_plug * evcs_num]
    # time_slot 반영
    for i in range(len(ev_day)):
        ev_day['in'][i] = ev_day['in'][i] - np.floor(time_slot/60)
        ev_day['out'][i] = ev_day['out'][i] - np.floor(time_slot/60)
    # time slot 음수 --> 제거
        if ev_day['in'][i] <= 0:
            ev_day['in'][i] = 0
    ## 모델 선언
    m = gp.Model("Aggregator")
    
    ## 변수 선언
    Power_pos = [m.addVars(range(ev_day['dur'][vdx]), ub=evcs['Pmax'][vdx+(day*len(ev_day))], lb= 0, vtype = GRB.INTEGER) for vdx in range(len(ev_day))]
    Power_neg = [m.addVars(range(ev_day['dur'][vdx]), ub= 0, lb=evcs['Pmin'][vdx+(day*len(ev_day))], vtype = GRB.INTEGER) for vdx in range(len(ev_day))]
    
    for idx in range(len(ev_day)):
        SOC = ev_day['init'][idx]
        for t in range(ev_day['dur'][idx]):
            ## Constraint 1 : 충방전 동시에 되지 않게 하기
            m.addConstr(Power_pos[idx][t] * Power_neg[idx][t] == 0)
            
            ## Constraint 2 : SoC boundary
            SOC += Power_pos[idx][t] * ev_day['chg_eff'][idx]/100 + Power_neg[idx][t] * ev_day['dchg_eff'][idx]/100
            m.addConstr(SOC >= ev_day['min'][idx])
            m.addConstr(SOC <= ev_day['max'][idx])
            
        ## Cosntraint 3 : Target SoC
        m.addConstr(SOC >= ev_day['target'][idx])
        
    ## 목적함수: 시간별 에너지 비용(전력량요금) (최소화)
    obj1 = gp.quicksum(Power_pos[idx][t] * tou['ToU'][t] + Power_neg[idx][t] * tou['ToU'][t] for idx in range(len(ev_day)) for t in range(ev_day['dur'][idx]))
    
    
    m.setObjective(obj1 , GRB.MINIMIZE)
    m.optimize()
    # 결과 정리
    # 결과 출력(csv or excel)

    # - 출력하는 샘플 코드 구글에서 찾아서, 실행해보는 곳.

    # for vdx5 in range(len(EV)):
    #     for t5 in range(EV['in'][vdx5],EV['out'][vdx5]+1):
    #         Power[vdx5,t5] = int('%s %g' % ('', Power[vdx5,t5].X))

    # TEST = pd.DataFrame(columns = range(len(EV)+1), index = range(len(Tou)+1))

    # for vdx6 in range(len(EV)):
    #     for t6 in range(EV['in'][vdx6],EV['out'][vdx6]+1):
    #         A6 += Power[vdx6,t6]
    #         SOC = round(EV['init'][vdx6] + A6/EV['cap'][vdx6],2)
    #         TEST.loc[t6,vdx6] = SOC , Power[vdx6,t6]
    #     SOC = 0
    #     A6 = 0
        
    # TEST.loc[48,1] = SL

    # TEST.to_excel(excel_writer = 'TEST.xlsx')
    trigger = 1
    return [Power,trigger,evcs_tot,ev_count]