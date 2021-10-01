from flask import Flask, request, render_template, jsonify
from scipy.optimize import fsolve
import numpy as np
import pandas as pd

app = Flask(__name__)
class SmeCalculator:
    def __init__(self, PV, T, r, fee, second_period, r2):
        self.PV = PV
        self.T = T        
        self.fee = fee
        self.second_period = second_period
        self.n = 12 * self.T
        self.n2 = self.n - self.second_period + 1 
        self.r = r
        self.r2 = r2
        self.meanrate_1 = self.calcu_meanrate(self.n, self.r)
        self.meanrate_2 = self.calcu_meanrate(self.n2, self.r2)

    @staticmethod
    def calcu_meanrate(n, r):       
        meanrate = ((1 + r/12)**n * r/12) / ((1 + r/12)**n - 1)
        return meanrate
    
    def calcu_payment(self):  
        payment_list = []
        pv = self.PV
        FV = pv * self.meanrate_1
        rate = self.r
        for stage in range(1, self.n+1):           
            if stage == self.second_period:
                FV = pv * self.meanrate_2
                rate = self.r2                
            month_i = pv * rate/12
            month_v = FV - month_i
            pv = pv + month_i - FV              
            if stage == self.n:             
                month_v += pv
                FV += pv
                pv = 0
            payment_list.append([stage, month_v, month_i, FV, pv])        
        return payment_list
    
    def create_payment_df(self):
        payment_list = self.calcu_payment()        
        payment_data = pd.DataFrame(payment_list, columns=['期別', '應還本金', '應付利息', '應付本息','剩餘本金'])
        for c in payment_data.columns:
            payment_data[c] = payment_data[c].apply(lambda x: int(round(x, 0)))
            payment_data[c] = payment_data[c].apply(lambda x: format(x, ','))
        return payment_data
    
    def calcu_year_rate(self):
        payment_data = self.create_payment_df()
        payment_ary = payment_data['應付本息'].apply(lambda x: int(x.replace(',', ''))).values
        payment_ary = np.hstack((np.array(-(self.PV - self.fee)), payment_ary))
        year_rate = np.irr(payment_ary) * 12
        year_rate = round(year_rate, 6)
        year_rate *= 100        
        return year_rate
    
    def calcu_rev_rate(self):
        FV = self.PV * (self.r / 12)
        def func(v):
            x, = v.tolist()
            return [
                (sum([FV / (1 + x / 12) ** i for i in range(1, self.n + 1)])) + \
                (self.PV / (1 + x / 12) ** 12) - (self.PV - self.fee)
            ]
        year_rate = fsolve(func, [0.01])[0]
        year_rate = round(year_rate, 6)
        year_rate *= 100        
        return year_rate

@app.route('/', methods=['GET', 'POST'])
def caculator():
    if request.method == 'POST':  
        cal_type = request.values['type']
        PV = int(request.values['PV']) * 10000
        T = int(request.values['T']) 
        fee = int(request.values['fee'])
        r = float(request.values['r']) * 0.01
        r2 = 0 if request.values['r2'] == '' else float(request.values['r2']) * 0.01
        second_period = 0 if request.values['n_gap'] == '' else int(request.values['n_gap'])        
        calculator = SmeCalculator(PV, T, r, fee, second_period, r2)
        if cal_type == '1':            
            payment_data = calculator.create_payment_df()
            year_rate = calculator.calcu_year_rate()
            pay_data_json = payment_data.to_json(orient="split", force_ascii=False)
            return jsonify(
                table=pay_data_json, 
                ans=year_rate)
        else:
            year_rate = calculator.calcu_rev_rate()
            return jsonify(ans=year_rate)
    return render_template('index.html')
    
if __name__ == '__main__':
    app.run()