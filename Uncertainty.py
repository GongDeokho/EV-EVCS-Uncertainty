def pipeline(err_rate,ev_day,ev_num,evcs,evcs_num,evcs_plug):
    import numpy as np
    import pandas as pd
    
    #데이터 생성 개수
    n = len(ev_day)
    
    ## Error rate 발생 ( Normal Distribution )
    def norm_dist(err_rate,ev_day,n,evcs_num,evcs_plug):
        mu1 = 0 #error mean : in, out, init soc
        x1 = err_rate # error rate
        
        # in, out, init soc
        sigma1 = x1/1.96
        error_rate = np.zeros([1,3])
        ev_error = np.zeros([1,3])
        loop = n
        while len(ev_error) < n:
            data1 = mu1 + sigma1 * np.random.randn(loop,3)
            for i in range(loop):
                error_data = np.zeros([1,3])
                error_data[0,0] = round(ev_day['in'][i] * (100 + data1[i,0])/100)
                error_data[0,1] = round(ev_day['out'][i] * (100 + data1[i,1])/100)
                error_data[0,2] = ev_day['init'][i] * (100 + data1[i,2])/100
                
                if ev_error[0,0] == 0 and ev_error[0,1] == 0 and ev_error [0,2] == 0:
                    ev_error = error_data
                else:
                    ev_error = np.append(ev_error, error_data, axis = 0)         
                            
            #Abnormal Data
            find_err1 = np.argwhere(ev_error[:,1] - ev_error[:,0] < 0 ) # plug-time minus
            find_err2 = np.argwhere(ev_error[:,1] > 48) # plug-time over
            find_err3 = np.argwhere(ev_error[:,2] < 0) #SoC violence
            find_err4 = np.argwhere(ev_error[:,2] > 100) #SoC violence
            idx_error = np.vstack([find_err1, find_err2, find_err3, find_err4])
            ev_error = np.delete(ev_error,idx_error,0)
            
            if len(ev_error) >= n:
                break
            
            if len(ev_error) > n:
                for i in range(n+1,len(ev_error)):
                    np.delete(ev_error,i,0)
            
        ev_err = pd.DataFrame(np.zeros([n,3]),columns = ['in','out','init'])
        for i in range(n):
            ev_err['in'][i] = ev_error[i,0]
            ev_err['out'][i] = ev_error[i,1]
            ev_err['init'][i] = ev_error[i,2]

        #recovery time & communication delay : time slot ==> minute
        mu2 = 120 #error mean : time value(2 hour)
        sigma2 = x1/1.96
        loop = n
        time_error = np.round(mu2 + sigma2 * np.random.randn(loop,2))
        time_error2 = np.round(mu2 + sigma2 * np.random.randn(evcs_num,1))
        time_err = pd.DataFrame(np.zeros([n,2]),columns = ['ev_recover_time','communication_delay'])
        time_err2 = pd.DataFrame(np.zeros([evcs_num,1]),columns = ['evcs_recover_time'])
        for i in range(n):
            time_err['ev_recover_time'][i] = time_error[i,0]
            time_err['communication_delay'][i] = time_error[i,1]
        
        for i in range(evcs_num):
            time_err2['evcs_recover_time'][i] = time_error2[i,0]
        # Chg, Dchg Error : deviation ==> no positive
        x3 = 20 #deviation
        mu3 = -40
        sigma3 = x3/1.96
        error_rate = np.zeros([1,3])
        eff_error = np.zeros([1,3])
        loop = n
        while len(eff_error) < n:
            data3 = mu3 + sigma3 * np.random.randn(loop,2)
            for i in range(loop):
                error_data = np.zeros([1,2])
                error_data[0,0] = round(ev_day['chg_eff'][i] * (100 + data3[i,0])/100)
                error_data[0,1] = round(ev_day['dchg_eff'][i] * (100 + data3[i,1])/100)
                
                if eff_error[0,0] == 0 and eff_error[0,1] == 0 and eff_error [0,2] == 0:
                    eff_error = error_data
                else:
                    eff_error = np.append(eff_error, error_data, axis = 0)         
            
            if len(eff_error) >= n:
                break
            
            if len(eff_error) > n:
                for i in range(n+1,len(eff_error)):
                    np.delete(eff_error,i,0)
            
        eff_err = pd.DataFrame(np.zeros([n,2]),columns = ['chg_eff','dchg_eff'])
        for i in range(n):
            eff_err['chg_eff'][i] = eff_error[i,0]
            eff_err['dchg_eff'][i] = eff_error[i,1]

        ev_err = pd.concat([ev_err,time_err,eff_err,time_err],axis = 1)
        return(ev_err,time_err2)
    [ev_err,time_err2] = norm_dist(err_rate,ev_day,n,evcs_num,evcs_plug)
    # Binary error 발생 (binomial Distribution)
    def binom_dist(evcs_num,ev_num,ev_err,time_err2):
        evcs_err = pd.DataFrame(np.zeros([evcs_num,1]),columns = ['hardware_err'])
        batt_err = pd.DataFrame(np.zeros([n,1]),columns = ['battery_fault'])
        # communication err : evcs
        hard_err = np.random.binomial(1,0.03117,evcs_num) # 0.03117 = 282/(365*24)를 푸아송 분포로
        for i in range(evcs_num):
            evcs_err['hardware_err'][i] = hard_err[i]
        
        # # Battery Fault : ev
        # batt_error = np.random.binomial(1,0.0194,30) # 0.0194 = 4500 / 231,443
        # for i in range(n):
        #     batt_err['battery_fault'][i] = batt_error[i]
        # ev_err = pd.concat([ev_err,batt_err],axis = 1)
        evcs_err = pd.concat([evcs_err,time_err2],axis = 1)
        return(evcs_err, ev_err)
    [evcs_err, ev_err] = binom_dist(evcs_num,ev_num,ev_err,time_err2)

    return [evcs_err,ev_err]