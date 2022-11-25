def pipeline(ev_day,ev_num,evcs,evcs_plug,evcs_num,trigger,tou,day,time_slot):
    import pandas as pd
    import gurobipy as gp
    from gurobipy import GRB

    ## 데이터 전처리
    SOC = 0
    # 충전기 개수만큼 ev 준비
    if ev_num >= evcs_plug:
        ev_day = ev_day[ev_day['ID'] <= evcs_plug]
    # time_slot 반영
    for i in range(len(ev_day)):
        ev_day['in'][i] = ev_day['in'][i] - time_slot
        ev_day['out'][i] = ev_day['out'][i] - time_slot
    # time slot 음수 --> 제거
        if ev_day['in'][i] <= 0:
            ev_day['in'][i] = 0
    ## 모델 선언
    m = gp.Model("Aggregator")
    
    ## 변수 선언
    Power_pos = [m.addVars(range(ev_day['dur'][vdx]), ub=evcs['Pmax'][vdx+(day*len(ev_day))], lb= 0, vtype = GRB.INTEGER) for vdx in range(len(ev_day))]
    Power_neg = [m.addVars(range(ev_day['dur'][vdx]), ub= 0, lb=evcs['Pmin'][vdx+(day*len(ev_day))], vtype = GRB.INTEGER) for vdx in range(len(ev_day))]
    
    ## Constraint 1 : SoC boundary
    for idx in range(len(ev_day)):
        SOC = ev_day['init'][idx]
        for time in range(ev_day['dur'][idx]):
            SOC += Power_pos[idx][time] * ev_day['chg_eff'][idx]/100 + Power_neg[idx][time] * ev_day['dchg_eff'][idx]/100
            m.addConstr(SOC >= ev_day['min'][idx])
            m.addConstr(SOC <= ev_day['max'][idx])
        ## Cosntraint 2 : Target SoC
        m.addConstr(SOC >= ev_day['target'][idx])
        SOC = 0
        
    ## Constraint 3 : 충방전 동시에 되지 않게 하기
    for idx in range(len(ev_day)):
        for time in range(ev_day['dur'][idx]):
            m.addConstr(Power_pos[idx][time] * Power_neg[idx][time] == 0)
            # m.addConstr(Power_pos[idx][time] * Power_neg[idx][time] >= 0)
    
    ## 목적함수: 시간별 에너지 비용(전력량요금) (최소화)
    obj1 = gp.quicksum(Power_pos[idx][time] * tou['ToU'][time] + Power_neg[idx][time] * tou['ToU'][time] for idx in range(len(ev_day)) for time in range(ev_day['dur'][idx]))

    m.setObjective(obj1 , GRB.MINIMIZE )

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
    return [Power,trigger]