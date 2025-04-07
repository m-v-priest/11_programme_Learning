import numpy as np
from dataclasses import dataclass
from typing import Dict, List
import random


@dataclass
class EconomicPolicy:
    """
    国家经济政策设置（新增关税和社会保险金比例）
    """
    interest_rate: float = 0.05  # 基准利率
    tax_rate: float = 0.2  # 平均税率
    tariff_rate: float = 0.1  # 平均关税税率（新增）
    military_spending: float = 0.1  # 军费占GDP比例
    education_spending: float = 0.05  # 教育投入比例
    tech_spending: float = 0.03  # 科技投入比例
    social_insurance: float = 0.08  # 社会保险金占GDP比例（新增）


@dataclass
class PopulationStructure:
    """
    人口年龄结构（新增人均寿命）
    """
    children: float = 0.2  # 0-14岁
    youth: float = 0.3  # 15-29岁
    adults: float = 0.35  # 30-59岁
    elderly: float = 0.15  # 60+岁
    life_expectancy: float = 70.0  # 人均寿命（岁）（新增）

    @property
    def aging_ratio(self):
        """老龄化比率"""
        return self.elderly / (self.children + self.youth + self.adults + self.elderly)


class CountryEconomy:
    """
    国家经济系统（增强版）
    新增功能：
    1. 关税对贸易的影响
    2. 社会保险系统
    3. 人均寿命动态模型
    """

    def __init__(self, name: str, initial_gdp: float, population: int):
        self.name = name
        self.gdp = initial_gdp
        self.population = population
        self.policy = EconomicPolicy()
        self.population_struct = PopulationStructure()
        self.war_damage = 0.0  # 战争破坏程度（0-1）

        # 经济状态变量
        self.inflation = 0.02
        self.unemployment = 0.05
        self.cpi = 100.0
        self.ppi = 100.0

        # 贸易数据（考虑关税影响）
        self.exports = self.gdp * 0.2 * (1 - self.policy.tariff_rate * 0.3)  # 关税会影响出口竞争力
        self.imports = self.gdp * 0.18 * (1 + self.policy.tariff_rate * 0.5)  # 关税会抑制进口

        # 历史数据
        self.gdp_history = [initial_gdp, initial_gdp]
        self.inflation_history = [0.02, 0.02]
        self.life_expectancy_history = [70.0, 70.0]

    @property
    def effective_social_spending(self):
        """实际社保支出（考虑战争影响）"""
        base = self.gdp * self.policy.social_insurance
        return base * (1 - self.war_damage * 0.5)  # 战争破坏会减少社保支出

    def update_life_expectancy(self):
        """更新人均寿命（系统动力学模型）"""
        # 基础影响因素
        gdp_impact = 0.05 * (self.gdp_per_capita / 1000)  # 每1000钱人均GDP增加0.05岁
        social_impact = 0.1 * (self.policy.social_insurance / 0.08)  # 基准社保比例增加0.1岁
        war_impact = -2.0 * self.war_damage  # 战争破坏每10%减少0.2岁

        # 医疗技术进步影响（随时间缓慢增加）
        tech_impact = 0.02 * (self.policy.tech_spending / 0.03)

        # 环境因素（GDP增长过快可能带来污染）
        env_impact = -0.01 * max(0, self.get_gdp_growth_rate() - 5)  # 增长率超过5%时产生负面影响

        # 计算新的人均寿命
        new_life = self.population_struct.life_expectancy + (
                gdp_impact + social_impact + war_impact + tech_impact + env_impact
        )

        # 限制在合理范围内
        self.population_struct.life_expectancy = max(50, min(85, new_life))
        self.life_expectancy_history.append(self.population_struct.life_expectancy)

    def adjust_tariff_based_on_trade(self):
        """根据贸易平衡自动调整关税（系统自动调节机制）"""
        trade_ratio = self.trade_deficit_ratio  # 贸易逆差率

        # 逆差较大时提高关税（上限30%）
        if trade_ratio > 0.1:  # 逆差超过10%
            self.policy.tariff_rate = min(0.3, self.policy.tariff_rate + 0.01)
        # 顺差较大时降低关税（下限2%）
        elif trade_ratio < -0.05:  # 顺差超过5%
            self.policy.tariff_rate = max(0.02, self.policy.tariff_rate - 0.005)

    def update_economy(self):
        """更新经济状态（增强版）"""
        # 原有经济更新逻辑...

        # 新增关税对贸易的影响（弹性模型）
        export_elasticity = -0.3  # 出口对关税的弹性
        import_elasticity = 0.5  # 进口对关税的弹性
        self.exports *= (1 + export_elasticity * (self.policy.tariff_rate - 0.1))
        self.imports *= (1 + import_elasticity * (0.1 - self.policy.tariff_rate))

        # 自动调整关税
        self.adjust_tariff_based_on_trade()

        # 更新人均寿命
        self.update_life_expectancy()

        # 社保支出对经济的影响
        social_impact = -0.001 * (self.policy.social_insurance - 0.08)  # 社保支出每增加1%，GDP增长减少0.001%

        # 将社保影响加入GDP计算
        base_growth = 0.03 + social_impact
        gdp_growth = (base_growth + aging_impact + ...)  # 原有其他影响因素

        # 战争破坏恢复（每月修复1%）
        self.war_damage = max(0, self.war_damage - 0.01)

    def apply_war_impact(self, damage: float):
        """应用战争影响"""
        self.war_damage = min(1.0, self.war_damage + damage)

        # 战争直接GDP损失（5%-15%）
        self.gdp *= 1 - (0.05 + damage * 0.1)

        # 战争导致失业率上升（2%-10%）
        self.unemployment = min(0.25, self.unemployment + 0.02 + damage * 0.08)

        # 更新人均寿命（战争立即影响）
        self.update_life_expectancy()


class WarSimulator:
    """战争模拟系统（增强版）"""

    @staticmethod
    def simulate_war(attacker: CountryEconomy, defender: CountryEconomy):
        """模拟战争并返回双方损失"""
        # 战争强度计算（基于军费比例和GDP）
        war_intensity = min(1.0,
                            (attacker.policy.military_spending + defender.policy.military_spending) / 0.2
                            )

        # 双方损失（攻击方损失较小）
        attacker_damage = 0.1 * war_intensity * random.uniform(0.8, 1.2)
        defender_damage = 0.2 * war_intensity * random.uniform(0.8, 1.2)

        # 应用战争影响
        attacker.apply_war_impact(attacker_damage)
        defender.apply_war_impact(defender_damage)

        # 战败方额外损失（可能失去领土）
        if defender_damage > 0.3:  # 严重破坏
            lost_gdp_share = defender_damage * 0.5  # 可能失去50%破坏程度的GDP比例
            defender.gdp *= (1 - lost_gdp_share)
            attacker.gdp *= (1 + lost_gdp_share * 0.8)  # 战胜方获得部分资源

            # 战败方社保系统崩溃（临时降低社保支出）
            defender.policy.social_insurance *= 0.7

        return {
            "attacker_damage": attacker_damage,
            "defender_damage": defender_damage,
            "war_intensity": war_intensity
        }


class ThreeKingdomsEconomyGame:
    """游戏主类（增强版）"""

    def next_month(self):
        """进入下个月（增强版）"""
        # 原有逻辑...

        # 随机战争事件（20%几率）
        if random.random() < 0.2:
            attacker, defender = random.sample([self.wei, self.shu, self.wu], 2)
            war_result = WarSimulator.simulate_war(attacker, defender)

            print(f"\n战争爆发！{attacker.name国家名字}攻击{defender.name国家名字}！")
            print(f"战争强度: {war_result['war_intensity']:.1f}")
            print(f"{attacker.name国家名字}损失: {war_result['attacker_damage'] * 100:.1f}%")
            print(f"{defender.name国家名字}损失: {war_result['defender_damage'] * 100:.1f}%")

    def display_status(self, country: CountryEconomy):
        """显示状态（增强版）"""
        # 原有显示...
        print(f"关税税率: {country.policy.tariff_rate * 100:.1f}%")
        print(f"社保支出: {country.effective_social_spending / country.gdp * 100:.1f}% of GDP")
        print(f"人均寿命: {country.population_struct.life_expectancy:.1f}岁")
        print(f"战争破坏: {country.war_damage * 100:.1f}%")