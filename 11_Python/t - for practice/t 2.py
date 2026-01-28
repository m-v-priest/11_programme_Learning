import numpy as np
from dataclasses import dataclass
from typing import Dict, List
import random


@dataclass
class ClsEconomicPolicy经济政策设置类:
    """
    国家经济政策设置
    """
    interest_rate: float = 0.05  # 基准利率
    tax_rate: float = 0.2  # 平均税率
    military_spending: float = 0.1  # 军费占GDP比例
    education_spending: float = 0.05  # 教育投入比例
    tech_spending: float = 0.03  # 科技投入比例


@dataclass
class ClsPopulationStructure人口年龄结构类:
    """
    人口年龄结构
    """
    children儿童占总人口比例: float = 0.2  # 0-14岁
    youth年轻人占总人口比例: float = 0.3  # 15-29岁
    adults成年人占总人口比例: float = 0.35  # 30-59岁
    elderly老年人占总人口比例: float = 0.15  # 60+岁

    @property
    def fn_aging_ratio获取老龄化比例(self):
        """老龄化比率"""
        return self.elderly老年人占总人口比例 / (self.children儿童占总人口比例 + self.youth年轻人占总人口比例 + self.adults成年人占总人口比例 + self.elderly老年人占总人口比例)


class ClsCountryEconomy国家经济参数系统类:
    """
    国家经济系统
    使用系统动力学模型模拟经济运行
    """

    def __init__(self, name: str, initial_gdp: float, population: int):
        self.name国家名字 = name
        self.gdp = initial_gdp
        self.population = population
        self.ins_policy经济政策设置类实例 = ClsEconomicPolicy经济政策设置类()
        self.ins_population_struct年龄人口结构实例 = ClsPopulationStructure人口年龄结构类()

        # 经济状态变量
        self.inflation通胀率 = 0.02  # 初始通胀率2%
        self.unemployment失业率 = 0.05  # 初始失业率5%
        self.cpi = 100.0  # 消费者价格指数
        self.ppi = 100.0  # 生产者价格指数

        # 贸易数据
        self.exports出口额 = self.gdp * 0.2  # 初始出口占GDP20%
        self.imports进口额 = self.gdp * 0.18  # 初始进口占GDP18%

        # 历史数据记录
        self.list_gdp_history = [initial_gdp, initial_gdp]  # 初始两个相同值，避免计算增长率时出错
        self.list_inflation_history通胀历年数据 = [0.02, 0.02]

    @property
    def fn_gdp_per_capita计算人均gdp(self):
        """人均GDP"""
        return self.gdp / self.population if self.population > 0 else 0

    @property
    def fn_income_per_capita计算人均收入(self):
        """人均收入"""
        return self.fn_gdp_per_capita计算人均gdp * 0.4  # 假设收入占GDP40%

    @property
    def disposable_income(self):
        """人均可支配收入"""
        return self.fn_income_per_capita计算人均收入 * (1 - self.ins_policy经济政策设置类实例.tax_rate)

    @property
    def fn_employment_rate计算就业率(self):
        """就业率"""
        return 1 - self.unemployment失业率

    @property
    def fn_trade_balance计算贸易顺差(self):
        """贸易差额(出口-进口)"""
        return self.exports出口额 - self.imports进口额

    @property
    def fn_trade_surplus_ratio计算贸易顺差率(self):
        """贸易顺差率"""
        total_trade进口与出口总额 = self.exports出口额 + self.imports进口额
        if total_trade进口与出口总额 == 0:
            return 0
        return (self.exports出口额 - self.imports进口额) / total_trade进口与出口总额

    @property
    def fn_trade_deficit_ratio计算贸易逆差率(self):
        """贸易逆差率"""
        total_trade进口与出口总额 = self.exports出口额 + self.imports进口额
        if total_trade进口与出口总额 == 0:
            return 0
        return (self.imports进口额 - self.exports出口额) / total_trade进口与出口总额

    @property
    def fn_military_pop_ratio计算军队占人口比率(self):
        """军队占总人口比例"""
        return 0.01 * (self.ins_policy经济政策设置类实例.military_spending / 0.05)  # 基准1%，随军费增加

    def fn_get_gdp_growth_rate计算gdp增长率(self):
        """获取GDP增长率"""
        if len(self.list_gdp_history) < 2:
            return 0.0
        return (self.list_gdp_history[-1] / self.list_gdp_history[-2] - 1) * 100

    def fn_update_economy更新经济数据(self):
        """
        更新经济状态 - 系统动力学模型核心
        实现经济参数间的相互影响关系
        """
        # 1. 计算GDP增长率影响因素
        aging_impact = -0.01 * self.ins_population_struct年龄人口结构实例.fn_aging_ratio获取老龄化比例  # 老龄化负面影响. 计算人口老龄化对经济增长的负面影响. 0.01：表示老龄化比率每增加1%，GDP增长减少0.01%. aging_ratio：老龄化人口占比（60岁以上人口比例）
        interest_impact = -0.005 * (self.ins_policy经济政策设置类实例.interest_rate - 0.05)  # 利率影响. 计算利率政策对经济增长的影响. 0.005：利率每偏离"基准利率"1%，GDP增长就变化0.005%. 0.05：设定的基准利率5%
        military_impact = -0.003 * (self.ins_policy经济政策设置类实例.military_spending - 0.1)  # 军费影响. 计算军费开支对经济增长的影响. 0.003：军费占比每偏离基准1%，GDP增长变化0.003%. 0.1：设定的基准军费占比10%
        tech_impact = 0.002 * (self.ins_policy经济政策设置类实例.tech_spending / 0.03)  # 科技投入正面影响. 计算科技投入对经济增长的正面影响. 0.002：科技投入带来的GDP增长系数. 0.03：设定的基准科技投入占比3%.


        # 基础增长率 + 各种影响因子.  这四种影响因子最终会汇总到GDP增长率的计算中
        base_growth = 0.03  # 基础年增长率3%
        gdp_growth = (base_growth +
                      aging_impact +
                      interest_impact +
                      military_impact +
                      tech_impact +
                      random.uniform(-0.01, 0.01))  # 随机波动
        '''
        老龄化每增加1% → GDP增长减少0.01%
        利率每高于基准1% → GDP增长减少0.005%
        军费每高于基准1% → GDP增长减少0.003%
        科技投入每增加1% → GDP增长增加0.002%
        '''

        # 2. 更新GDP
        self.gdp *= (1 + gdp_growth)
        self.list_gdp_history.append(self.gdp)

        # 3. 更新通胀率 (菲利普斯曲线关系) : 在经济复苏的时候，企业要招更多的人，就要提高工资水平以和其他企业竞争，表现为名义工资上升(通胀率上升)、失业率下降的负相关性。即, 通胀率和失业率, 成反比关系. 这个意思是什么呢? 这就意味着要想通胀率下降, 就要付出失业率上升的代价. 反之依然.  两者不能两全. 低失业率和低通胀, 不可能同时实现, 鱼和熊掌不可兼得. 反之, 高失业率和高通胀, 也不太可能一起出现.

        inflation_base = 0.02  # 基础通胀率2%. 设定一个经济体的长期平均通胀率（央行通胀目标）. 它将作为通胀率的基准值，其他影响因素会在此基础上叠加
        unemployment_impact = 0.005 * (0.05 - self.unemployment失业率)  # 失业率影响.
        '''
        0.05：代表​​自然失业率​​（Non-Accelerating Inflation Rate of Unemployment, NAIRU）
        (0.05 - self.unemployment)：失业率(self.unemployment)与自然失业率(0.05)的差距. 如果失业率(self.unemployment)提高, 则这个差的结果,就为正数, 则  unemployment_impact 就为正数.   如果失业率(self.unemployment)下降,小于自然失业率0.05, 则这个差的结果,就为负数.
        当失业率 < 自然失业率的5%时 → unemployment_impact的值为正 → 推高通胀
        当失业率 > 自然失业率的5%时 → unemployment_impact的值为负 → 抑制通胀
        0.005：调节系数，表示失业率每偏离自然失业率1%，通胀率变化0.5%
        
        经济学解释​​（菲利普斯曲线）：
        ​​失业率↓ → 劳动力市场紧张 → 工资上涨 → 生产成本↑ → 物价↑​​
        ​​失业率↑ → 劳动力过剩 → 工资增长停滞 → 物价压力↓​
        '''
        self.inflation通胀率 = inflation_base + unemployment_impact + random.uniform(-0.005, 0.005) # 失业率低于5%时推高通胀, 失业率高于5%时抑制通胀
        '''
        通胀率合成​
        三部分叠加​​：
            inflation_base：长期基础通胀
            unemployment_impact：失业率带来的周期性波动
            random.uniform(-0.005, 0.005)：随机扰动（模拟外部冲击）
        经济学意义​​：
            实际通胀 = 目标通胀 + 经济周期影响 + 随机冲击
            体现了"通胀既受系统性因素影响，也有不可预测波动"的现实特征
            
        代码对应的经济学逻辑​​
        ​​当失业率 = 5%时​​
                unemployment_impact = 0
                通胀率 = 2%（基础值）± 随机波动
        ​​当失业率 = 3%时​​（低于自然率）
                unemployment_impact = 0.005*(0.05-0.03) = 0.0001
                通胀率 ≈ 2.01% + 随机波动
                经济过热导致轻微通胀压力
        ​​当失业率 = 7%时​​（高于自然率）
                unemployment_impact = 0.005*(0.05-0.07) = -0.0001
                通胀率 ≈ 1.99% + 随机波动
                经济衰退带来通缩压力
        '''


        self.list_inflation_history通胀历年数据.append(self.inflation通胀率)

        # 4. 更新价格指数
        self.cpi *= (1 + self.inflation通胀率)
        self.ppi *= (1 + self.inflation通胀率 * 0.8)  # PPI通常波动小于CPI

        # 5. 更新失业率 (奥肯定律). 奥肯法则（Okun's Law），也称为奥肯定律，指的是实际经济增长率与失业率变动之间的反向相关关系，即经济增长率越高，失业率就越低。 尽管奥肯法则在西方国家获得了较好的验证，但在中国大陆，GDP增长和失业率变动的关系一直不显著，这也引发了许多讨论。有学者认为这其中包含失业率对整体就业水平的不完全体现。在中国官方统计失业率属于城镇人口调查失业率，而在经济周期性衰退中丢掉工作的往往是进城务工的农民工，但这个数量庞大的群体却并不在失业率的统计当中。
        unemployment_change = (0.05 - self.unemployment失业率) * 0.2  # 向自然失业率回归
        '''
        0.05​​：自然失业率（NAIRU），即经济长期均衡时的失业率
        ​​(0.05 - self.unemployment)​​：当前失业率与自然失业率的差距
        当失业率 > 5% → 负值 → 推动失业率下降
        当失业率 < 5% → 正值 → 推动失业率上升
        ​​* 0.2​​：调节系数，表示每月向"自然失业率"回归20%的差距
        ​​经济学意义​​：
        "失业率有自发回归"自然水平"的趋势，如同弹簧的恢复力"
        '''

        gdp_impact = -0.02 * (gdp_growth - 0.03)  # 增长高于趋势则失业下降
        '''
        GDP增长对失业率的影响（奥肯定律核心）​
        ​​0.03​​：潜在GDP增长率（基准值）
        ​​(gdp_growth - 0.03)​​：实际增长率与潜在增长率的差距
        增长 > 3% → 正值 → 降低失业率
        增长 < 3% → 负值 → 提高失业率
        ​​-0.02​​：奥肯系数，表示GDP增长率每超过潜在增长率1%，失业率下降0.02%（约合现实中的0.3-0.5%比例缩放）
        ​​奥肯定律公式​​：
        Δ失业率 = -k × (实际GDP增长率 - 潜在GDP增长率)
        其中k是经验系数（此处为0.02）
        '''

        self.unemployment失业率 += unemployment_change + gdp_impact
        '''
        综合更新失业率​
        双重影响叠加​​：
            unemployment_change：自然回归力
            gdp_impact：经济增长的拉动/拖累
        '''

        self.unemployment失业率 = max(0.02, min(0.15, self.unemployment失业率))  # 保持在2%-15%之间. min() 方法返回给定参数中的最小值，参数可以为序列。



        # 6. 更新贸易数据
        export_growth = gdp_growth * 1.1 + random.uniform(-0.02, 0.02)
        import_growth = gdp_growth * 0.9 + random.uniform(-0.02, 0.02)
        self.exports出口额 *= (1 + export_growth)
        self.imports进口额 *= (1 + import_growth)

        # 7. 人口结构缓慢变化
        self.ins_population_struct年龄人口结构实例.elderly老年人占总人口比例 += 0.002  # 老龄化每年增加0.2%
        self.ins_population_struct年龄人口结构实例.children儿童占总人口比例 = max(0.15, self.ins_population_struct年龄人口结构实例.children儿童占总人口比例 - 0.001)

        # 8. 人口增长 (与GDP增长相关)
        pop_growth = 0.01 + (gdp_growth - 0.03) * 0.2  # 基础1%，随经济增长变化
        self.population = int(self.population * (1 + pop_growth))

    def adjust_policy(self, interest_change=0, tax_change=0, military_change=0):
        """
        调整经济政策
        参数为变化量，如+0.01表示增加1个百分点
        """
        self.ins_policy经济政策设置类实例.interest_rate = max(0, min(0.2, self.ins_policy经济政策设置类实例.interest_rate + interest_change))
        self.ins_policy经济政策设置类实例.tax_rate = max(0.1, min(0.5, self.ins_policy经济政策设置类实例.tax_rate + tax_change))
        self.ins_policy经济政策设置类实例.military_spending = max(0.01, min(0.3, self.ins_policy经济政策设置类实例.military_spending + military_change))

        # 政策调整会影响市场信心
        if interest_change < 0 or tax_change < 0:
            self.gdp *= 1.005  # 宽松政策短期刺激经济
        elif interest_change > 0 or tax_change > 0:
            self.gdp *= 0.995  # 紧缩政策短期抑制经济


class ClsInternationalTrade国际贸易系统类:
    """
    国际贸易系统
    模拟国家间的经济互动
    作用​​：创建一个管理多国汇率和贸易的系统
    """

    def __init__(self, list_countries国家经济参数实例: List[ClsCountryEconomy国家经济参数系统类]):
        # countries - 国家经济对象列表（如[魏国, 蜀国, 吴国]）

        self.dict_countries各国名字与其经济参数实例的键值对 = {c.name国家名字: c for c in list_countries国家经济参数实例} # 这里创建了一个dict字典, key就是特定国家的名字, value就是该国的"经济参数实例"
        '''
        数据结构​​：将国家列表转为{国家名: 国家对象}的字典
        （例如 {"魏": wei_obj, "蜀": shu_obj}）
        ​​目的​​：快速通过国家名访问经济数据
        '''

        self.dict_exchange_rates各国间汇率系统字典 = {}  # 空字典. 汇率矩阵.  格式: {(国家A,国家B): 汇率} <- dict的 key,可以是一个元组类型

        '''        
        汇率定义​​：
        1单位A货币 = X单位B货币
        例如 ("魏","蜀")=1.5,  表示: 1魏币=1.5蜀币
        
        该"dict_exchange_rates各国间汇率系统字典", 最终会是比如:
        {
         ("魏","魏"): 1.0,  
         ("魏","蜀"): 1.6,  ("蜀","魏"): 0.625,  # 1/1.6
         ("魏","吴"): 0.8,  ("吴","魏"): 1.25,   # 1/0.8
         ("蜀","吴"): 1.2,  ("吴","蜀"): 0.833   # 1/1.2
        }
        '''


        # 初始化随机汇率
        list_names各国名字 = [c.name国家名字 for c in list_countries国家经济参数实例]
        for i, c1 in enumerate(list_names各国名字):
            for j, c2 in enumerate(list_names各国名字):
                if i == j: # 相同国家
                    self.dict_exchange_rates各国间汇率系统字典[(c1, c2)] = 1.0  # 自兑换汇率为1, 即本"国的货币"兑换"本国的货币", 那汇率肯定是1:1了
                elif i < j:  # 避免重复计算
                    rate随机汇率 = random.uniform(0.5, 2.0) # 随机初始汇率. uniform() 方法将随机生成下一个实数，它在 [x, y] 范围内。如, uniform(5, 10) 的随机数为 :  6.98774810047.
                    # 随机设定在0.5~2.0之间，模拟现实中的汇率差异. （例如：1魏币=0.8吴币，1魏币=1.8蜀币）
                    self.dict_exchange_rates各国间汇率系统字典[(c1, c2)] = rate随机汇率 # 将随机汇率, 赋值给c1,c2这两个国家货币的 汇率交换值.
                    self.dict_exchange_rates各国间汇率系统字典[(c2, c1)] = 1 / rate随机汇率 # 反向汇率. 反向汇率通过倒数自动计算 （若 魏/蜀=1.5 → 则 蜀/魏=1/1.5≈0.67）

        '''
        关键设计​​：
        -​​对角线元素(i=j)​​
        任何国家与自身的汇率, 都是1:1
        （如 ("魏","魏")=1.0）
        
        -​​"非对称"汇率关系​​
        只计算i<j的组合（避免重复生成"魏-蜀"和"蜀-魏"）
        反向汇率, 通过"倒数"自动计算
        （若 魏/蜀=1.5 → 则 蜀/魏=1/1.5≈0.67）
        
        ​-​"初始汇率"范围​​
        随机设定在0.5~2.0之间，模拟现实中的汇率差异
        （例如：1魏币=0.8吴币，1魏币=1.8蜀币）
        '''

    def update_trade(self):
        """
        更新国际贸易关系
        包括汇率变化和贸易量调整

        这段代码是​​"国际贸易系统"的动态更新方法​​，实现了两个核心经济机制：​"​汇率浮动机制"​​和​​"贸易量自适应调整"​​。
        """
        # 1. 更新汇率 (基于相对经济表现)
        list_names各国名字 = list(self.dict_countries各国名字与其经济参数实例的键值对.keys()) # 将dict中的key, 即各国名字, 放在一个list中.

        for i, c1 in enumerate(list_names各国名字):
            for j, c2 in enumerate(list_names各国名字):
                if i < j:
                    #  计算两国GDP增长率差异, 经济表现好的国家货币升值.
                    growth_diff两国GDP增长率差异 = (self.dict_countries各国名字与其经济参数实例的键值对[c1].fn_get_gdp_growth_rate计算gdp增长率() -
                                   self.dict_countries各国名字与其经济参数实例的键值对[c2].fn_get_gdp_growth_rate计算gdp增长率()) / 100
                    '''
                    growth_diff = (c1最新GDP/c1上期GDP - c2最新GDP/c2上期GDP)  
                    '''

                    change对汇率的影响度 = growth_diff两国GDP增长率差异 * 0.1  # gdp增长率差异中的10%, 会影响汇率
                    # 若c1比c2经济增长快1%，则c1货币升值0.1%（系数0.1控制敏感度）. 例如：魏国GDP增长5%，蜀国增长3% → 魏币对蜀币升值0.2%


                    # 更新汇率
                    self.dict_exchange_rates各国间汇率系统字典[(c1, c2)] *= (1 + change对汇率的影响度)
                    self.dict_exchange_rates各国间汇率系统字典[(c2, c1)] = 1 / self.dict_exchange_rates各国间汇率系统字典[(c1, c2)] # 保持A→B和B→A汇率的数学倒数关系

                    '''
                    关键逻辑：
                    -​​相对增长决定汇率​​
                    若c1比c2经济增长快1%，则c1货币升值0.1%（系数0.1控制敏感度）
                    例如：魏国GDP增长5%，蜀国增长3% → 魏币对蜀币升值0.2%
                    
                    -​​双向汇率同步更新​​
                    保持A→B和B→A汇率的数学倒数关系
                    
                    -​​经济学原理​​
                    模仿现实中的"经济增长→资本流入→货币升值"机制
                    类似人民币升值与中国经济高速增长的关系
                    
                    '''

        # 2. 贸易量自动调整 (基于相对价格和汇率)
        for country in self.dict_countries各国名字与其经济参数实例的键值对.values():
            # 出口公式. 出口竞争力受汇率和PPI影响
            export_factor = (1 / self.dict_exchange_rates各国间汇率系统字典[(country.name国家名字, "魏")]) * (100 / country.ppi)  #  export_factor = (1/该国对魏汇率) * (100/该国PPI)
            country.exports出口额 *= (0.9 + 0.2 * export_factor)

            # 进口公式. 进口需求受收入和汇率影响
            import_factor = country.disposable_income * self.dict_exchange_rates各国间汇率系统字典[(country.name国家名字, "魏")] # import_factor = 该国人均可支配收入 * 该国对魏汇率
            country.imports进口额 *= (0.95 + 0.1 * import_factor)


class ThreeKingdomsEconomyGame:
    """
    三国经济模拟游戏
    """

    def __init__(self):
        # 初始化三个国家
        self.wei = ClsCountryEconomy国家经济参数系统类("魏", initial_gdp=1000, population=1000000)
        self.shu = ClsCountryEconomy国家经济参数系统类("蜀", initial_gdp=800, population=800000)
        self.wu = ClsCountryEconomy国家经济参数系统类("吴", initial_gdp=900, population=900000)

        # 设置初始差异
        self.wei.ins_policy经济政策设置类实例.tech_spending = 0.04  # 魏国科技投入更高
        self.shu.ins_policy经济政策设置类实例.education_spending = 0.07  # 蜀国教育投入更高
        self.wu.ins_policy经济政策设置类实例.military_spending = 0.15  # 吴国军费更高

        # 国际贸易系统
        self.trade_system = ClsInternationalTrade国际贸易系统类([self.wei, self.shu, self.wu])

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
        self.wei.fn_update_economy更新经济数据()
        self.shu.fn_update_economy更新经济数据()
        self.wu.fn_update_economy更新经济数据()

        # 更新国际贸易
        self.trade_system.update_trade()

    def display_status(self, country: ClsCountryEconomy国家经济参数系统类):
        """显示国家经济状况"""
        print(f"\n{country.name国家名字}国 {self.year}年{self.month}月经济状况:")
        print(f"GDP: {country.gdp:.2f}亿钱 (增长率: {country.fn_get_gdp_growth_rate计算gdp增长率():.1f}%)")
        print(f"人均GDP: {country.fn_gdp_per_capita计算人均gdp:.2f}钱")
        print(f"通胀率: {country.inflation通胀率 * 100:.1f}% CPI: {country.cpi:.1f} PPI: {country.ppi:.1f}")
        print(f"失业率: {country.unemployment失业率 * 100:.1f}% 就业率: {country.fn_employment_rate计算就业率 * 100:.1f}%")
        print(f"贸易顺差率: {country.fn_trade_surplus_ratio计算贸易顺差率 * 100:.1f}% 军队比例: {country.fn_military_pop_ratio计算军队占人口比率 * 100:.1f}%")
        print(f"老龄化率: {country.ins_population_struct年龄人口结构实例.fn_aging_ratio获取老龄化比例 * 100:.1f}%")
        print(f"当前政策: 利率{country.ins_policy经济政策设置类实例.interest_rate * 100:.1f}% 税率{country.ins_policy经济政策设置类实例.tax_rate * 100:.1f}%")

    def player_adjust_policy(self, country: ClsCountryEconomy国家经济参数系统类):
        """玩家调整政策"""
        print("\n可调整政策:")
        print(f"1. 调整利率 (当前: {country.ins_policy经济政策设置类实例.interest_rate * 100:.1f}%)")
        print(f"2. 调整税率 (当前: {country.ins_policy经济政策设置类实例.tax_rate * 100:.1f}%)")
        print(f"3. 调整军费比例 (当前: {country.ins_policy经济政策设置类实例.military_spending * 100:.1f}%)")
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
                print(f"魏国 GDP: {self.wei.gdp:.2f}亿 增长率: {self.wei.fn_get_gdp_growth_rate计算gdp增长率():.1f}%")
                print(f"吴国 GDP: {self.wu.gdp:.2f}亿 增长率: {self.wu.fn_get_gdp_growth_rate计算gdp增长率():.1f}%")
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