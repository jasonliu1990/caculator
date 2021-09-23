from flask import Flask, jsonify, request
import math 
import numpy as np
import pandas as pd

app = Flask(__name__)

def calcu_rate(PV, T, m, n_gap, r, r2, fee):
    
    output_data = {}
    n = m * T
    # 每月應付本息金額之平均攤還率
    meanrate = ((1 + r/12)**n * r/12) / ((1 + r/12)**n - 1)
    #平均每月應攤付本息總額
    FV = round(PV * meanrate, 0)
    # 總費用年百分率
    year_rate = round(np.rate(n, -FV, (PV - fee), 0) * 12, 4)
    
    output_data['FV1'] = FV
    output_data['year_rate'] = year_rate

    pay_list = []
    for j in range(1, n+1):    
        
        # 第二段利率
        if j == n_gap:
            r = r2
            n2 = n - n_gap + 1
            meanrate = ((1 + r/12)**n2 * r/12) / ((1 + r/12)**n2 - 1)
            FV = round(PV * meanrate, 0)
            output_data['FV2'] = FV

        #每月應付利息金額
        month_i = PV * r/12
        #每月應付本息金額 : FV    
        #每月應還本金金額
        month_v = FV - month_i
        PV = PV + month_i - FV      

        # 最後一期作調整
        if j == n:             
            month_v += PV
            FV += PV
            PV = 0
        pay_list.append([j, month_v, month_i, FV, PV])
        
    pay_data = pd.DataFrame(pay_list, columns=['期別', '應還本金', '應付利息', '應付本息','剩餘本金'])
    
    return pay_data, output_data

@app.route('/caculator', methods=['POST'])
def caculator():
    # try:
    param = request.get_json(force=True)
    print(param)
    pay_data, output_data = calcu_rate(param['PV'], param['T'], param['m'], param['n_gap'], param['r'], param['r2'], param['fee'])
    
    
    return jsonify(
        {'yearRate': output_data['year_rate']}
    ) 
    # except Exception as e:
    # 	return jsonify(
    #     	{'message': str(e)}
    #     ) 
    
if __name__ == '__main__':
    app.run()
    debug = True