from scipy import stats
import pandas as pd
import numpy as np
import QuantLib as ql
import math

#quantlib库 BS方法实现欧式期权公式法定价
def bsm_quantlib():
    # 1.设置期权的五要素以及分红率和期权类型
    # 1.1五要素
    maturity_date = ql.Date(31, 7, 2020)
    spot_price = 9.37
    strike_price = 10.00
    volatility = 0.20  # the historical vols for a year
    risk_free_rate = 0.001
    # 1.2分红率
    dividend_rate = 0.01
    # 1.3期权类型
    option_type = ql.Option.Call

    # 1.4设置日期计算方式与使用地区
    day_count = ql.Actual365Fixed()
    calendar = ql.UnitedStates()
    # 1.5计算期权价格的日期，也就是估值日，我们设为今天
    calculation_date = ql.Date(31, 7, 2019)
    ql.Settings.instance().evaluationDate = calculation_date
    # 2.利用上的设置配置一个欧式期权
    payoff = ql.PlainVanillaPayoff(option_type, strike_price)
    exercise = ql.EuropeanExercise(maturity_date)
    # 2.1根据payoff与exercise完成欧式期权的构建
    european_option = ql.VanillaOption(payoff, exercise)

    # 3.构造我们的BSM定价引擎
    # 3.1 处理股票当前价格
    spot_handle = ql.QuoteHandle( ql.SimpleQuote(spot_price))
    # 3.2 根据之前的无风险利率和日期计算方式，构建利率期限结构
    flat_ts = ql.YieldTermStructureHandle( ql.FlatForward(calculation_date, risk_free_rate, day_count))
    # 3.3 设置分红率期限结构
    dividend_yield = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, dividend_rate, day_count))
    # 3.4 设置波动率结构
    flat_vol_ts = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(calculation_date, calendar, volatility, day_count))
    # 3.5 构造BSM定价引擎
    bsm_process = ql.BlackScholesMertonProcess(spot_handle, dividend_yield, flat_ts,flat_vol_ts)

    # 4使用BSM定价引擎计算
    european_option.setPricingEngine(ql.AnalyticEuropeanEngine(bsm_process))
    #bs_price = european_option.NPV()
    #print"The theoretical price is ", bs_price

    # RESULTS
    print("Option value =", european_option.NPV())
    print("Delta value  =", european_option.delta())
    print("Theta value  =", european_option.theta())
    print("Theta perday =", european_option.thetaPerDay())
    print("Gamma value  =", european_option.gamma())
    print("Vega value   =", european_option.vega())
    print("Rho value    =", european_option.rho())
class Option(object):
    def __init__(self,S0, K, T, r, sigma, type, M):
        """
         Parameters:
         ==========
         S0: float
             标 的物初始价格水平
         K: float
             行权价格
         T: float
             到期日
         r: float
             无风险利率
         sigma: float
             波动因子
        type: : string
            either 'call' or 'put'
        M : int
        number of time intervals
         Returns
         ==========
         value: float
         """
        self.S0 = S0
        self.K = K
        self.T = T
        self.r = r
        self.sigma=sigma
        self.type=type
        self.M = M

    # 欧式期权定价公式
    def bsm_price(self):
        self.S0 = float(self.S0)
        d1 = (np.log(self.S0 / self.K) + (self.r + 0.5 * self.sigma ** 2) *self.T) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)
        # 欧式看涨期权的价值
        value1 = self.S0 * stats.norm.cdf(d1, 0, 1) - self.K * np.exp(-self.r * self.T) * stats.norm.cdf(d2, 0, 1)
        # 欧式看跌期权的价值
        value2 = - self.S0 * stats.norm.cdf(-d1, 0, 1) + self.K * np.exp(-self.r * self.T) * stats.norm.cdf(-d2, 0, 1)
        #print(value1, value2)
        return(value1)

    # 欧式期权 二叉树方法
    def CRR_european_option_value(self):
        # 生成二叉树
        dt = self.T / self.M  # length of time interval
        df = math.exp(-self.r * dt)  # discount per interval
        u = math.exp(self.sigma * math.sqrt(dt))
        d = 1 / u  # down movement
        q = (math.exp(self.r * dt) - d) / (u - d)  # martingale branch probability\n",
        # 初始化幂矩阵
        mu = np.arange(self.M + 1)
        mu = np.resize(mu, (self.M + 1, self.M + 1))
        #print(mu)
        md = np.transpose(mu)

        mu = u ** (mu - md)
        md = d ** md
        #得到各节点的股票价格\n",
        S = self.S0 * mu * md #目标二叉树
        # 得到叶子结点的期权价值\n",
        if self.type == 'call':
            V = np.maximum(S - self.K, 0)  # inner values for European call option
        else:
            V = np.maximum(self.K - S, 0)  # inner values for European put option\n",
        #逐步向前加权平均并折现，得到期初期权价值
        for z in range(0, self.M):  # backwards iteration
            #逐列更新期权价值，相当于二叉树中的逐层向前折算
            V[0:self.M - z, self.M - z - 1] = (q * V[0:self.M - z, self.M - z] +(1 - q) * V[1:self.M - z + 1, self.M - z]) * df
        #print("Option value =", V[0, 0])
        return V[0, 0]
    #期权价格变化 = 标的价格变化*delta
    def delta(self):
        ds = 0.1
        new = Option(self.S0, self.K, self.T, self.r, self.sigma, self.type, self.M)
        new1 = Option(self.S0+ds, self.K, self.T, self.r, self.sigma, self.type, self.M)
        #print("Delta value  =", (new1.CRR_european_option_value() - new.CRR_european_option_value()) / ds)
        return (new1.CRR_european_option_value() - new.CRR_european_option_value()) / ds
    #delta的导数，delta的变化敏感程度
    def gamma(self):
        ds = 0.1
        new = Option(self.S0, self.K, self.T, self.r, self.sigma, self.type, self.M)
        new1 = Option(self.S0+ds, self.K, self.T, self.r, self.sigma, self.type, self.M)
        #print("Gamma value  =", (new1.delta() - new.delta()) / ds)
        return (new1.delta() - new.delta()) / ds
    #隐含波动率对期权价格的影响
    def vega(self):
        dsigma = 0.0001
        new = Option(self.S0, self.K, self.T, self.r, self.sigma, self.type, self.M)
        new1 = Option(self.S0, self.K, self.T, self.r, self.sigma+dsigma, self.type, self.M)
        #print("vega value  =", (new1.CRR_european_option_value() - new.CRR_european_option_value()) / dsigma / 100)
        return (new1.CRR_european_option_value() - new.CRR_european_option_value()) / dsigma / 100
    #期权价格随时间损耗速度，时间价值衰减
    def theta(self):
        dt = 0.0001
        new = Option(self.S0, self.K, self.T, self.r, self.sigma, self.type, self.M)
        new1 = Option(self.S0, self.K, self.T+dt, self.r, self.sigma, self.type, self.M)
        #print("theta value  =", -(new1.CRR_european_option_value() - new.CRR_european_option_value()) / dt)
        return -(new1.CRR_european_option_value() - new.CRR_european_option_value()) / dt
    #衡量期权价格较利率变化的敏感程度
    def rho(self):
        dr = 0.0001
        new = Option(self.S0, self.K, self.T, self.r, self.sigma, self.type, self.M)
        new1 = Option(self.S0, self.K, self.T, self.r+dr, self.sigma, self.type, self.M)
        #print("rho value  =", (new1.CRR_european_option_value() - new.CRR_european_option_value()) / dr / 100)
        return (new1.CRR_european_option_value() - new.CRR_european_option_value()) / dr / 100

    #期权价格变化 = 标的价格变化*delta
    def delta_bsm(self):
        ds = 0.1
        new = Option(self.S0, self.K, self.T, self.r, self.sigma, self.type, self.M)
        new1 = Option(self.S0+ds, self.K, self.T, self.r, self.sigma, self.type, self.M)
        #print("Delta value  =", (new1.CRR_european_option_value() - new.CRR_european_option_value()) / ds)
        return (new1.bsm_price() - new.bsm_price()) / ds
    #delta的导数，delta的变化敏感程度
    def gamma_bsm(self):
        ds = 0.1
        new = Option(self.S0, self.K, self.T, self.r, self.sigma, self.type, self.M)
        new1 = Option(self.S0+ds, self.K, self.T, self.r, self.sigma, self.type, self.M)
        #print("Gamma value  =", (new1.delta() - new.delta()) / ds)
        return (new1.delta_bsm() - new.delta_bsm()) / ds
    #隐含波动率对期权价格的影响
    def vega_bsm(self):
        dsigma = 0.0001
        new = Option(self.S0, self.K, self.T, self.r, self.sigma, self.type, self.M)
        new1 = Option(self.S0, self.K, self.T, self.r, self.sigma+dsigma, self.type, self.M)
        #print("vega value  =", (new1.CRR_european_option_value() - new.CRR_european_option_value()) / dsigma / 100)
        return (new1.bsm_price() - new.bsm_price()) / dsigma / 100
    #期权价格随时间损耗速度，时间价值衰减
    def theta_bsm(self):
        dt = 0.0001
        new = Option(self.S0, self.K, self.T, self.r, self.sigma, self.type, self.M)
        new1 = Option(self.S0, self.K, self.T+dt, self.r, self.sigma, self.type, self.M)
        #print("theta value  =", -(new1.CRR_european_option_value() - new.CRR_european_option_value()) / dt)
        return -(new1.bsm_price() - new.bsm_price()) / dt
    #衡量期权价格较利率变化的敏感程度
    def rho_bsm(self):
        dr = 0.0001
        new = Option(self.S0, self.K, self.T, self.r, self.sigma, self.type, self.M)
        new1 = Option(self.S0, self.K, self.T, self.r+dr, self.sigma, self.type, self.M)
        #print("rho value  =", (new1.CRR_european_option_value() - new.CRR_european_option_value()) / dr / 100)
        return (new1.bsm_price() - new.bsm_price()) / dr / 100

def main():
    p = Option(50,50,5, 0.10, 0.50, "call", 30)
    print("Option value  =",p.CRR_european_option_value())
    #p.CRR_european_option_value()
    print("delta value  =", p.delta())
    print("gamma value  =", p.gamma())
    print("vega value  =", p.vega())
    print("theta value  =", p.theta())
    print("rho value  =", p.rho())

    print("bsm Option value  =", p.bsm_price())
    print("bsm delta value  =", p.delta_bsm())
    print("bsm gamma value  =", p.gamma_bsm())
    print("bsm vega value  =", p.vega_bsm())
    print("bsm theta value  =", p.theta_bsm())
    print("bsm rho value  =", p.rho_bsm())
if __name__ == '__main__':
    main()