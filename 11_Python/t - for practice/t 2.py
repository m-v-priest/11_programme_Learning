import numpy as np
from dataclasses import dataclass
from typing import Dict, List
import random


@dataclass
class EconomicPolicy:
    """
    国家经济政策设置
    """
    interest_rate: float = 0.05  # 基准利率
    tax_rate: float = 0.2  # 平均税率
    military_spending: float = 0.1  # 军费占GDP比例
    education_spending: float = 0.05  # 教育投入比例
    tech_spending: float = 0.03  # 科技投入比例


@dataclass
class PopulationStructure:
    """
    人口年龄结构
    """
    children: float = 0.2  # 0-14岁
    youth: float = 0.3  # 15-29岁
    adults: float = 0.35  # 30-59岁
    elderly: float = 0.15  # 60+岁

    @property
    def aging_ratio(self):
        """老龄化比率"""
        return self.elderly / (self.children + self.youth + self.adults + self.elderly)


class CountryEconomy:
    """
    国家经济系统
    使用系统动力学模型模拟经济运行
    """

    def __init__(self, name: str, initial_gdp: float, population: int):
        self.name = name
        self.gdp = initial_gdp
        self.population = population
        self.policy = EconomicPolicy()
        self.population_struct = PopulationStructure()

        # 经济状态变量
        self.inflation = 0.02  # 初始通胀率2%
        self.unemployment = 0.05  # 初始失业率5%
        self.cpi = 100.0  # 消费者价格指数
        self.ppi = 100.0  # 生产者价格指数

        # 贸易数据
        self.exports = self.gdp * 0.2  # 初始出口占GDP20%
        self.imports = self.gdp * 0.18  # 初始进口占GDP18%

        # 历史数据记录
        self.gdp_history = [initial_gdp]
        self.inflation_history = [0.02]

    @property
    def gdp_per_capita(self):
        """人均GDP"""
        return self.gdp / self.population

    @property
    def income_per_capita(self):
        """人均收入"""
        return self.gdp_per_capita * 0.4  # 假设收入占GDP40%

    @property
    def disposable_income(self):
        """人均可支配收入"""
        return self.income_per_capita * (1 - self.policy.tax_rate)

    @property
    def employment_rate(self):
        """就业率"""
        return 1 - self.unemployment

    @property
    def trade_balance(self):
        """贸易差额(出口-进口)"""
        return self.exports - self.imports

    @property
    def trade_surplus_ratio(self):
        """贸易顺差率"""
        total_trade = self.exports + self.imports
        if total_trade == 0:
            return 0
        return (self.exports - self.imports) / total_trade

    @property
    def trade_deficit_ratio(self):
        """贸易逆差率"""
        total_trade = self.exports + self.imports
        if total_trade == 0:
            return 0
        return (self.imports - self.exports) / total_trade

    @property
    def military_pop_ratio(self):
        """军队占总人口比例"""
        return 0.01 * (self.policy.military_spending / 0.05)  # 基准1%，随军费增加

    def update_economy(self):
        """
        更新经济状态 - 系统动力学模型核心
        实现经济参数间的相互影响关系
        """
        # 1. 计算GDP增长率影响因素
        aging_impact = -0.01 * self.population_struct.aging_ratio  # 老龄化负面影响
        interest_impact = -0.005 * (self.policy.interest_rate - 0.05)  # 利率影响
        military_impact = -0.003 * (self.policy.military_spending - 0.1)  # 军费影响
        tech_impact = 0.002 * (self.policy.tech_spending / 0.03)  # 科技投入正面影响

        # 基础增长率 + 各种影响因子
        base_growth = 0.03  # 基础年增长率3%
        gdp_growth = (base_growth +
                      aging_impact +
                      interest_impact +
                      military_impact +
                      tech_impact +
                      random.uniform(-0.01, 0.01))  # 随机波动

        # 2. 更新GDP
        self.gdp *= (1 + gdp_growth)
        self.gdp_history.append(self.gdp)

        # 3. 更新通胀率 (菲利普斯曲线关系)
        inflation_base = 0.02  # 基础通胀率2%
        unemployment_impact = 0.005 * (0.05 - self.unemployment)  # 失业率影响
        self.inflation = inflation_base + unemployment_impact + random.uniform(-0.005, 0.005)
        self.inflation_history.append(self.inflation)

        # 4. 更新价格指数
        self.cpi *= (1 + self.inflation)
        self.ppi *= (1 + self.inflation * 0.8)  # PPI通常波动小于CPI

        # 5. 更新失业率 (奥肯定律)
        unemployment_change = (0.05 - self.unemployment) * 0.2  # 向自然失业率回归
        gdp_impact = -0.02 * (gdp_growth - 0.03)  # 增长高于趋势则失业下降
        self.unemployment += unemployment_change + gdp_impact
        self.unemployment = max(0.02, min(0.15, self.unemployment))  # 保持在2%-15%之间

        # 6. 更新贸易数据
        export_growth = gdp_growth * 1.1 + random.uniform(-0.02, 0.02)
        import_growth = gdp_growth * 0.9 + random.uniform(-0.02, 0.02)
        self.exports *= (1 + export_growth)
        self.imports *= (1 + import_growth)

        # 7. 人口结构缓慢变化
        self.population_struct.elderly += 0.002  # 老龄化每年增加0.2%
        self.population_struct.children = max(0.15, self.population_struct.children - 0.001)

        # 8. 人口增长 (与GDP增长相关)
        pop_growth = 0.01 + (gdp_growth - 0.03) * 0.2  # 基础1%，随经济增长变化
        self.population = int(self.population * (1 + pop_growth))

    def adjust_policy(self, interest_change=0, tax_change=0, military_change=0):
        """
        调整经济政策
        参数为变化量，如+0.01表示增加1个百分点
        """
        self.policy.interest_rate = max(0, min(0.2, self.policy.interest_rate + interest_change))
        self.policy.tax_rate = max(0.1, min(0.5, self.policy.tax_rate + tax_change))
        self.policy.military_spending = max(0.01, min(0.3, self.policy.military_spending + military_change))

        # 政策调整会影响市场信心
        if interest_change < 0 or tax_change < 0:
            self.gdp *= 1.005  # 宽松政策短期刺激经济
        elif interest_change > 0 or tax_change > 0:
            self.gdp *= 0.995  # 紧缩政策短期抑制经济


class InternationalTrade:
    """
    国际贸易系统
    模拟国家间的经济互动
    """

    def __init__(self, countries: List[CountryEconomy]):
        self.countries = {c.name: c for c in countries}
        self.exchange_rates = {}  # 汇率矩阵

        # 初始化随机汇率
        names = [c.name for c in countries]
        for i, c1 in enumerate(names):
            for j, c2 in enumerate(names):
                if i == j:
                    self.exchange_rates[(c1, c2)] = 1.0
                elif i < j:
                    rate = random.uniform(0.5, 2.0)
                    self.exchange_rates[(c1, c2)] = rate
                    self.exchange_rates[(c2, c1)] = 1 / rate

    def update_trade(self):
        """
        更新国际贸易关系
        包括汇率变化和贸易量调整
        """
        # 1. 更新汇率 (基于相对经济表现)
        names = list(self.countries.keys())
        for i, c1 in enumerate(names):
            for j, c2 in enumerate(names):
                if i < j:
                    # 经济表现好的国家货币升值
                    growth_diff = (self.countries[c1].list_gdp_history[-1] / self.countries[c1].list_gdp_history[-2] -
                                   self.countries[c2].list_gdp_history[-1] / self.countries[c2].list_gdp_history[-2])
                    change = growth_diff * 0.1  # 增长率差异的10%影响汇率
                    self.exchange_rates[(c1, c2)] *= (1 + change)
                    self.exchange_rates[(c2, c1)] = 1 / self.exchange_rates[(c1, c2)]

        # 2. 贸易量自动调整 (基于相对价格和汇率)
        for country in self.countries.values():
            # 出口竞争力受汇率和PPI影响
            export_factor = (1 / self.exchange_rates[(country.name, "魏")]) * (100 / country.ppi)
            country.exports出口额 *= (0.9 + 0.2 * export_factor)

            # 进口需求受收入和汇率影响
            import_factor = country.fn_disposable_income计算人均可支配收入 * self.exchange_rates[(country.name, "魏")]
            country.imports进口额 *= (0.95 + 0.1 * import_factor)


class ThreeKingdomsEconomyGame:
    """
    三国经济模拟游戏
    """

    def __init__(self):
        # 初始化三个国家
        self.wei = CountryEconomy("魏", initial_gdp=1000, population=1000000)
        self.shu = CountryEconomy("蜀", initial_gdp=800, population=800000)
        self.wu = CountryEconomy("吴", initial_gdp=900, population=900000)

        # 设置初始差异
        self.wei.policy.tech_spending = 0.04  # 魏国科技投入更高
        self.shu.policy.education_spending = 0.07  # 蜀国教育投入更高
        self.wu.policy.military_spending = 0.15  # 吴国军费更高

        # 国际贸易系统
        self.trade_system = InternationalTrade([self.wei, self.shu, self.wu])

        # 游戏时间
        self.year = 190
        self.month = 1

    def next_month(self):
        """进入下个月"""
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1

        # 更新各国经济
        self.wei.update_economy()
        self.shu.update_economy()
        self.wu.update_economy()

        # 更新国际贸易
        self.trade_system.update_trade()

    def display_status(self, country: CountryEconomy):
        """显示国家经济状况"""
        print(f"\n{country.name}国 {self.year}年{self.month}月经济状况:")
        print(f"GDP: {country.gdp:.2f}亿钱 (增长率: {(country.gdp / country.gdp_history[-2] - 1) * 100:.1f}%)")
        print(f"人均GDP: {country.gdp_per_capita:.2f}钱")
        print(f"通胀率: {country.inflation * 100:.1f}% CPI: {country.cpi:.1f} PPI: {country.ppi:.1f}")
        print(f"失业率: {country.unemployment * 100:.1f}% 就业率: {country.employment_rate * 100:.1f}%")
        print(f"贸易顺差率: {country.trade_surplus_ratio * 100:.1f}% 军队比例: {country.military_pop_ratio * 100:.1f}%")
        print(f"老龄化率: {country.population_struct.aging_ratio * 100:.1f}%")
        print(f"当前政策: 利率{country.policy.interest_rate * 100:.1f}% 税率{country.policy.tax_rate * 100:.1f}%")

    def player_adjust_policy(self, country: CountryEconomy):
        """玩家调整政策"""
        print("\n可调整政策:")
        print(f"1. 调整利率 (当前: {country.policy.interest_rate * 100:.1f}%)")
        print(f"2. 调整税率 (当前: {country.policy.tax_rate * 100:.1f}%)")
        print(f"3. 调整军费比例 (当前: {country.policy.military_spending * 100:.1f}%)")
        print("4. 返回")

        choice = input("选择操作: ")
        try:
            if choice == "1":
                change = float(input("输入利率变化(+/-百分点，如1.5或-0.5): ")) / 100
                country.adjust_policy(interest_change=change)
            elif choice == "2":
                change = float(input("输入税率变化(+/-百分点): ")) / 100
                country.adjust_policy(tax_change=change)
            elif choice == "3":
                change = float(input("输入军费比例变化(+/-百分点): ")) / 100
                country.adjust_policy(military_change=change)
        except ValueError:
            print("请输入有效数字!")

    def main_loop(self):
        """游戏主循环"""
        print("三国经济模拟游戏 - 系统动力学模型")
        print("你将管理蜀国的经济政策")

        while True:
            self.display_status(self.shu)

            print("\n1. 调整经济政策")
            print("2. 查看其他国家")
            print("3. 进入下个月")
            print("4. 退出游戏")

            choice = input("选择操作: ")
            if choice == "1":
                self.player_adjust_policy(self.shu)
            elif choice == "2":
                print("\n其他国家经济概况:")
                print(
                    f"魏国 GDP: {self.wei.gdp:.2f}亿 增长率: {(self.wei.gdp / self.wei.gdp_history[-2] - 1) * 100:.1f}%")
                print(f"吴国 GDP: {self.wu.gdp:.2f}亿 增长率: {(self.wu.gdp / self.wu.gdp_history[-2] - 1) * 100:.1f}%")
                input("\n按回车键继续...")
            elif choice == "3":
                self.next_month()
            elif choice == "4":
                break
            else:
                print("无效输入!")


# 启动游戏
if __name__ == "__main__":
    game = ThreeKingdomsEconomyGame()
    game.main_loop()