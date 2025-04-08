import numpy as np
from typing import Dict, List


class City:
    def __init__(self, name: str, params: Dict):
        self.name = name
        self.params = {
            'population': params['population'],
            'gdp': params['gdp'],
            'industry_mix': params.get('industry_mix', [0.3, 0.4, 0.3]),
            'infrastructure': params.get('infrastructure', 0.7)
        }

    def update(self, national_effects: Dict):
        # 人口迁移模型（简化版）
        migration_factor = 0.01 * (self.params.get('gdp_per_capita', 0) - national_effects['national_gdp_pc'])
        self.params['population'] *= (1 + migration_factor + national_effects['population_growth'])

        # 城市GDP增长计算
        infrastructure_effect = 0.2 * (self.params['infrastructure'] - 0.5)
        self.params['gdp'] *= (1 + national_effects['gdp_growth'] / 100 + infrastructure_effect)

        # 更新人均GDP
        if self.params['population'] > 0:
            self.params['gdp_per_capita'] = self.params['gdp'] / self.params['population']


class Country:
    def __init__(self, name: str, params: Dict):
        self.name = name
        self.params = params.copy()
        self.history = []

        # 设置默认参数
        self.params.setdefault('population_growth', 0.01)  # 默认年人口增长率1%
        self.params.setdefault('aging_ratio', 0.15)

        # 初始化5个城市
        self.cities = [
            City(f"{name} City {i + 1}", {
                'population': self.params['population'] / 5,
                'gdp': self.params['gdp'] / 5
            }) for i in range(5)
        ]

    def update(self, global_effects: Dict):
        self.aggregate_city_data()
        self.calculate_demographics()  # 新增人口动态计算
        self.calculate_gdp_growth()
        self.update_labor_market()
        self.update_fiscal()
        self.history.append(self.params.copy())

    def aggregate_city_data(self):
        """聚合城市数据到国家层面"""
        total_pop = sum(c.params['population'] for c in self.cities)
        total_gdp = sum(c.params['gdp'] for c in self.cities)
        self.params['population'] = total_pop
        self.params['gdp'] = total_gdp
        self.params['gdp_per_capita'] = total_gdp / total_pop if total_pop > 0 else 0

    def calculate_demographics(self):
        """人口动态计算（新增关键模块）"""
        # 人口增长率 = 自然增长率 + 移民净流量
        fertility = 1.5 - 0.02 * self.params['gdp_per_capita'] / 1e4  # 生育率随人均GDP下降
        mortality = 7.0 + 0.5 * self.params['aging_ratio']  # 死亡率随老龄化上升

        natural_growth = (fertility - mortality) / 1000
        self.params['population_growth'] = natural_growth + 0.002 * np.random.normal()

        # 更新老龄化比例
        self.params['aging_ratio'] = min(0.5, self.params['aging_ratio'] + 0.001)

    def calculate_gdp_growth(self):
        """基于扩展生产函数的GDP计算"""
        alpha = 0.3  # 资本产出弹性
        beta = 0.6  # 劳动产出弹性

        # 劳动力增长 = 人口增长 × 劳动参与率
        labor_growth = self.params['population_growth'] * (1 - self.params['aging_ratio'])
        capital_growth = 0.05 * self.params.get('investment_ratio', 0.2)

        # 全要素生产率增长
        tfp_growth = 0.01 + 0.03 * self.params.get('rd_ratio', 0.02)

        self.params['gdp_growth_rate'] = (
                alpha * capital_growth +
                beta * labor_growth +
                tfp_growth +
                np.random.normal(0, 0.005)
        )
        self.params['gdp'] *= (1 + self.params['gdp_growth_rate'])


class InternationalSystem:
    def __init__(self, countries: List[Country]):
        self.countries = {c.name: c for c in countries}

    def simulate_year(self):
        global_growth = self.calculate_global_growth()
        for country in self.countries.values():
            country.update({
                'global_growth': global_growth,
                'commodity_prices': np.random.normal(100, 10)
            })

    def calculate_global_growth(self) -> float:
        total_gdp = sum(c.params['gdp'] for c in self.countries.values())
        weights = [c.params['gdp'] / total_gdp for c in self.countries.values()]
        return sum(c.params['gdp_growth_rate'] * w for c, w in zip(self.countries.values(), weights))


# 正确初始化国家（包含所有必要参数）
usa = Country("United States", {
    'gdp': 21.43e12,
    'population': 331e6,
    'investment_ratio': 0.2,
    'rd_ratio': 0.03,
    'aging_ratio': 0.16,
    'population_growth': 0.007  # 明确设置初始人口增长率
})

china = Country("China", {
    'gdp': 14.34e12,
    'population': 1.4e9,
    'investment_ratio': 0.25,
    'rd_ratio': 0.02,
    'aging_ratio': 0.12,
    'population_growth': 0.004
})

# 模拟运行
world = InternationalSystem([usa, china])
for year in range(2023, 2025):
    print(f"\n=== Year {year} ===")
    world.simulate_year()

    for country in world.countries.values():
        print(f"\n{country.name}:")
        print(f"GDP: ${country.params['gdp'] / 1e12:.2f}T")
        print(f"GDP Growth: {country.params['gdp_growth_rate'] * 100:.2f}%")
        print(f"Population: {country.params['population'] / 1e6:.1f}M")
        print(f"Aging Ratio: {country.params['aging_ratio'] * 100:.1f}%")