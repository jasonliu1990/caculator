from flask import Flask, request, render_template, jsonify
from scipy.optimize import fsolve
import numpy as np
import pandas as pd

app = Flask(__name__)

def calcu_rate(PV, T, r, fee, n_gap=0, r2=0):
    
    output_data = {}
    n = 12 * T
    # 每月應付本息金額之平均攤還率
    meanrate = ((1 + r/12)**n * r/12) / ((1 + r/12)**n - 1)
    #平均每月應攤付本息總額
    FV = round(PV * meanrate, 0)
    output_data['FV1'] = FV
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
    for c in pay_data.columns:
        pay_data[c] = pay_data[c].apply(lambda x: int(round(x, 0)))

    return pay_data, output_data

def rev_rate(PV, r, T, fee):
    n = T * 12
    FV = PV * (r / 12)
    def func(v):
        x, = v.tolist()
        return [
            (sum([FV / (1 + x / 12) ** i for i in range(1, n + 1)])) + (PV / (1 + x / 12) ** 12) - (PV - fee)
        ]
    year_rate = fsolve(func, [1])[0]

    return year_rate

@app.route('/', methods=['GET', 'POST'])
def caculator():
    if request.method == 'POST':
  
        cal_type = request.values['type']
        PV = int(request.values['PV']) * 10000
        T = int(request.values['T']) 
        r = float(request.values['r']) * 0.01
        fee = int(request.values['fee'])
        n_gap = 0 if request.values['n_gap'] == '' else int(request.values['n_gap'])
        r2 = 0 if request.values['r2'] == '' else float(request.values['r2']) * 0.01
              
        if cal_type == '2':
            year_rate = rev_rate(PV, r, T, fee)
            year_rate = round(year_rate, 4)
            year_rate *= 100
    
            return jsonify(ans=year_rate)

        else:
            pay_data, _ = calcu_rate(PV, T, r, fee, n_gap, r2)
            year_rate = (np.sum(pay_data['應付利息']) + fee) / (((np.sum(pay_data['剩餘本金']) + PV) / (12 * T))) / T
            year_rate = round(year_rate, 4)
            year_rate *= 100
            pay_data_json = pay_data.to_json(orient="split", force_ascii=False)

            return jsonify(
                table=pay_data_json, 
                ans=year_rate)

    return render_template('index.html')
    
if __name__ == '__main__':
    app.run()