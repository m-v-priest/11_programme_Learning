
import numpy as np  # 导入NumPy库，用于数值计算

class Country:
    def __init__(self, name, params):
        self.name = name  # 国家名称
        # 宏观经济参数初始化，若未提供则使用默认值
        self.interest_rate = params.get('interest_rate', 0.03)            # 利率
        self.tax_rate = params.get('tax_rate', 0.25)                      # 税率
        self.gdp = params.get('gdp', 1000.0)                              # 初始GDP值
        self.population = params.get('population', 50.0)                  # 初始人口（百万）
        self.capital_stock = params.get('capital_stock', 500.0)           # 初始资本存量
        self.productivity = params.get('productivity', 1.0)               # 全要素生产率
        self.inflation_rate = params.get('inflation_rate', 0.02)         # 通货膨胀率
        self.cpi = params.get('cpi', 100.0)                              # 消费者价格指数
        self.ppi = params.get('ppi', 100.0)                              # 工业品价格指数
        self.employment_rate = params.get('employment_rate', 0.95)       # 就业率
        self.age_structure = params.get('age_structure',
            {'0-14': 0.20, '15-64': 0.65, '65+': 0.15})                   # 年龄结构比例
        self.aging_ratio = self.age_structure['65+']                      # 老龄化比率
        self.military_gdp_ratio = params.get('military_gdp_ratio', 0.02) # 军费占GDP比
        self.military_population_ratio = params.get('military_population_ratio', 0.002)  # 军队占比
        # 贸易及财政参数
        self.exports = params.get('exports', 100.0)                      # 出口总额
        self.imports = params.get('imports', 90.0)                       # 进口总额
        self.birth_rate = params.get('birth_rate', 0.01)                 # 出生率
        self.death_rate = params.get('death_rate', 0.008)                # 死亡率
        self.savings_rate = params.get('savings_rate', 0.20)             # 储蓄率
        self.gov_spending_ratio = params.get('gov_spending_ratio', 0.20) # 政府支出占GDP比
        self.debt_gdp_ratio = params.get('debt_gdp_ratio', 0.50)        # 债务占GDP比

    def compute_gdp_growth(self):
        # 基于多种因素计算下一期GDP增长率（简单线性权重模型）
        base_growth = 0.03  # 潜在增长率
        growth = (
            base_growth
            - 0.5 * (self.interest_rate - 0.03)       # 利率上升抑制投资
            - 0.3 * (self.tax_rate - 0.25)            # 税率上升抑制消费
            - 0.4 * (self.inflation_rate - 0.02)      # 通胀过高降低实际购买力
            - 0.2 * (self.aging_ratio - 0.15)         # 老龄化加剧抑制劳动力
            - 0.1 * (self.military_gdp_ratio - 0.02)  # 军费过高占用资源
            + 0.5 * (self.productivity - 1.0)         # 生产率提升带动增长
        )
        return growth

    def update(self):
        # 更新所有经济指标
        gdp_growth = self.compute_gdp_growth()                      # 计算GDP增长率
        self.gdp *= (1 + gdp_growth)                                # 更新GDP
        # 人口随出生率和死亡率变化
        self.population *= (1 + self.birth_rate - self.death_rate)
        # 价格指数随通胀率变化
        self.cpi *= (1 + self.inflation_rate)
        self.ppi *= (1 + self.inflation_rate * 1.1)
        # 通胀率根据产出缺口调整
        self.inflation_rate = 0.02 + 0.5 * (gdp_growth - 0.03)
        # 就业率受GDP增长和通胀影响
        self.employment_rate = min(
            1.0,
            self.employment_rate + 0.3 * gdp_growth - 0.2 * self.inflation_rate
        )
        self.unemployment_rate = 1.0 - self.employment_rate          # 失业率
        # 贸易总额随全球需求变化
        self.exports *= (1 + 0.02 + 0.5 * gdp_growth)
        self.imports *= (1 + 0.025 + 0.4 * gdp_growth)
        # 计算贸易差率
        total_trade = self.exports + self.imports
        self.trade_surplus_rate = (self.exports - self.imports) / total_trade * 100
        self.trade_deficit_rate = (self.imports - self.exports) / total_trade * 100
        # 计算人均相关指标
        self.per_capita_gdp = self.gdp / self.population
        self.per_capita_income = self.per_capita_gdp * (1 - self.savings_rate)
        self.per_capita_disposable_income = self.per_capita_income * (1 - self.tax_rate)

    def report(self):
        # 返回当前各项指标的字典报告
        return {
            'GDP': round(self.gdp, 2),
            'GDP_growth_rate': round(self.compute_gdp_growth(), 4),
            'Population': round(self.population, 2),
            'Per_capita_GDP': round(self.per_capita_gdp, 2),
            'Per_capita_income': round(self.per_capita_income, 2),
            'Per_capita_disposable_income': round(self.per_capita_disposable_income, 2),
            'Inflation_rate': round(self.inflation_rate, 4),
            'CPI': round(self.cpi, 2),
            'PPI': round(self.ppi, 2),
            'Employment_rate': round(self.employment_rate, 4),
            'Unemployment_rate': round(self.unemployment_rate, 4),
            'Trade_surplus_rate': round(self.trade_surplus_rate, 2),
            'Trade_deficit_rate': round(self.trade_deficit_rate, 2),
            'Aging_ratio': round(self.aging_ratio, 4),
            'Military_GDP_ratio': round(self.military_gdp_ratio, 4),
            'Military_population_ratio': round(self.military_population_ratio, 4)
        }

# 示例：创建国家并模拟10年变化
if __name__ == '__main__':
    params = {}                         # 使用默认参数，也可传入自定义字典
    country = Country('StateA', params) # 实例化国家对象
    for year in range(1, 11):          # 模拟10个周期（可代表10年）
        country.update()                # 更新经济指标
        print(f'Year {year}:', country.report())  # 打印当年报告
