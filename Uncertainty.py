def pipeline(input_path,err_rate,ev_day,evcs):
    import numpy as np
    import pandas as pd
    
    n = len(ev_day)
    
    # Error rate 발생 ( Normal Distribution )
    mu = 0 #error mean
    x = err_rate # error rate
    
    sigma = x/1.96
    error_rate = np.zeros([1,3])
    ev_error = np.zeros([1,3])
    loop = n
    while len(ev_error) <= n:
        data = mu + sigma * np.random.randn(loop,3)
        for i in range(loop):
            error_data = np.zeros([1,3])
            error_data[0,0] = round(ev_day['in'][i] * (100 + data[i,0])/100)
            error_data[0,1] = round(ev_day['out'][i] * (100 + data[i,1])/100)
            error_data[0,2] = ev_day['init_soc'][i] * (100 + data[i,2])/100
            
            if ev_error[0,0] == 0 and ev_error[0,1] == 0 and ev_error [0,2] == 0:
                ev_error = error_data
            else:
                ev_error = np.append(ev_error, error_data, axis = 0)         
                        
        #Abnormal Data
        find_err1 = np.argwhere(ev_error[:,1] - ev_error[:,0] < 0 ) # plug-time minus
        find_err2 = np.argwhere(ev_error[:,1] > 48) # plug-time over
        find_err3 = np.argwhere(ev_error[:,2] < 0) #SoC violence
        find_err4 = np.argwhere(ev_error[:,2] > 1) #SoC violence
        idx_error = np.vstack([find_err1, find_err2, find_err3, find_err4])
        ev_error = np.delete(ev_error,idx_error,0)
        
        if len(ev_error) >= n:
            break
        
        if len(ev_error) > n:
            for i in range(n+1,len(ev_error)):
                np.delete(ev_error,i,0)
        
    ev_err = pd.DataFrame(np.zeros([n,3]),columns = ['in','out','init_soc'])
    for i in range(n):
        ev_err['in'][i] = ev_error[i,0]
        everr['out'][i] = ev_error[i,1]
        ev_err['init_soc'][i] = ev_error[i,2]
            
    # Binary error 발생 (poisson Distribution)
    
    
    
    
    return [evcs_err,ev_err]