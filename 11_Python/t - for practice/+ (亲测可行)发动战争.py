import random
from dataclasses import dataclass
from enum import Enum, auto


# 所有人才数据库, 放在一个dict中
# 所有城市数据库, 放在一个dict中

@dataclass
class Cls人才类:
    str人才名字: str
    int统帅值: int


@dataclass
class Cls城市类:
    str城市名: str
    int城市人口数: int
    str本城为谁控制: str
    str本城太守: str
    list人才实例: list[Cls人才类]  # 注意, 这里人才列表, 是个指针, 指向外面的真正人才列表数据


# 游戏状态枚举
class Cls游戏状态枚举(Enum):
    enum大地图模式 = auto()
    enum战争模式 = auto()


# 实例化人才类
insCls人才类_关羽 = Cls人才类("关羽", 90)
insCls人才类_张飞 = Cls人才类("张飞", 80)
insCls人才类_张辽 = Cls人才类("张辽", 85)
insCls人才类_徐晃 = Cls人才类("徐晃", 75)

# 实例化城市类
insCls城市类_成都 = Cls城市类("成都", 50000, "玩家", insCls人才类_关羽.str人才名字,
                              [insCls人才类_关羽, insCls人才类_张飞])
insCls城市类_许昌 = Cls城市类("许昌", 60000, "电脑", insCls人才类_张辽.str人才名字,
                              [insCls人才类_张辽, insCls人才类_徐晃])


# 主游戏类
class Cls游戏主控类:
    # 创建本类中的属性 ,并初始化它们, 作为游戏一开始的默认数据
    def __init__(self):
        # 先初始化游戏界面状态枚举.  进入游戏后, 首先让其处于大地图模式
        self.enum当前界面模式: Cls游戏状态枚举 = Cls游戏状态枚举.enum大地图模式

        # 初始化玩家控制的城市列表
        self.list玩家控制的城市实例列表: list[Cls城市类] = [insCls城市类_成都]  # 目前这个城市列表中, 只放了一个城市实例.

        # 初始化电脑控制的城市列表
        self.list电脑控制的城市实例列表: list[Cls城市类] = [insCls城市类_许昌]

        # 初始化游戏时间系统
        self.int当前月数 = 1

    def fn打印出所有势力控制的城市列表(self):
        print(f'玩家 控制的城市有: {self.list玩家控制的城市实例列表}')
        print(f'电脑 控制的城市有: {self.list电脑控制的城市实例列表}')

    def fn判定战争胜负(self, ins进攻方城市实例: Cls城市类, ins防守方城市实例: Cls城市类) -> str:
        # 这里, 其实应该传入: 进攻方和防守方, 各自的人才和城市数据. 判断公式, 用 进攻方的统帅值 + 军力  VS 防守方统帅值 + 城防
        # 但本练习中, 我们简单点操作, 就直接用随机数来决定, 从0个1两个里,随机挑选出一个数, 是0的话, 防守方赢; 是1的话, 进攻方赢.  此处,我们先不考虑平局这种情况.
        # 本方法, 会返回一个字符串, 指明是哪一方获胜的, 即返回 "进攻方"还是"防守方" 获胜.
        int结果 = random.randint(0, 1)
        if int结果 == 1:
            print(f"进攻方: {ins进攻方城市实例.str本城太守} 获胜")
            return "进攻方"  # 将哪一方获胜的信息, 返回
        else:
            print(f"防守方: {ins防守方城市实例.str本城太守} 获胜")
            return "防守方"  # 将哪一方获胜的信息, 返回

    def fn战争后的结果(self, str哪方获胜, ins进攻方城市实例: Cls城市类, ins防守方城市实例: Cls城市类):
        if str哪方获胜 == "进攻方":
            ins进攻方城市实例.int城市人口数 = int(
                ins防守方城市实例.int城市人口数 * 0.9)  # 攻击方损失10%人口.  对于有小数点的数值, int()会向下取整, 即 0.99 = 0
            ins防守方城市实例.int城市人口数 = int(
                ins防守方城市实例.int城市人口数 * 0.5)  # 防守方损失50%人口. 其实还可以让这里面逃难的人口, 分散到周边城市去.

            # 城市占领逻辑. 如果进攻方是玩家, 则玩家接管电脑(防守方, 失败方)控制的城市.
            if ins防守方城市实例.str本城为谁控制 == "电脑":
                ins防守方城市实例.str本城为谁控制 == "玩家"
                self.list玩家控制的城市实例列表.append(ins防守方城市实例)  # 玩家获得了新城市
                self.list电脑控制的城市实例列表.remove(ins防守方城市实例)  # 电脑失去了战败城市
                print(f"玩家占领了{ins防守方城市实例.str城市名}")
                self.fn打印出所有势力控制的城市列表()  # 显示目前新的势力控制状态

        else:  # 如果防守方获胜的话, 双方的城市控制, 没有变化
            # 这里我就不写具体的操作逻辑了, 你之后可以自己加上. 比如, 双方城市人口还是会有损失等等.
            print("防守方获胜")

    def fn玩家发动战争(self, ins进攻方城市实例: Cls城市类):
        # 先创建变量, 用来存储 防守方的城市实例
        ins进攻方城市实例: Cls城市类 = ins进攻方城市实例 # 接收本函数传入进来的参数
        ins防守方城市实例: Cls城市类 = object()  # 先用 object()函数, 它能返回一个空对象

        # 显示可攻击的敌人的城市目标
        print("\n可攻击的电脑城市有:")
        for intIndex, ins城市实例 in enumerate(self.list电脑控制的城市实例列表):
            print(f"{intIndex}. {ins城市实例.str城市名}. / 太守: {ins城市实例.str本城太守}")

        # 获取玩家所选择的index编号, 用来指明要攻击那座敌方城市
        try:
            int战争目标城市编号 = int(input("选择要攻击的城市(编号):"))
            ins防守方城市实例 = self.list电脑控制的城市实例列表[int战争目标城市编号]
            str战争结果 = self.fn判定战争胜负(ins进攻方城市实例, ins防守方城市实例)
            self.fn战争后的结果(str战争结果, ins进攻方城市实例,ins防守方城市实例)

        except ValueError:
            print("请输入有效数字!")


    def fn电脑发动战争(self):  # 这里的具体执行, 我就不写了
        print("★★★ 电脑向你发动战争")

    def fn进入下一个回合(self):
        self.int当前月数 += 1
        print(f"当前月数{self.int当前月数}")

        # 30%几率触发AI攻击
        int随机值 = random.random()
        print(f"随机值:{int随机值}")
        print("------")
        if int随机值 < 0.33:  # random.random()会返回一个0-1之间的浮点数.
            self.fn电脑发动战争()

    def fn游戏主循环(self):
        #游戏主循环
        while True:  # 一直保持循环, 根据游戏界面类型, 作为判断分支, 来进入相应要执行的函数方法中.
            if self.enum当前界面模式 == Cls游戏状态枚举.enum大地图模式:
                # 显示游戏大地图, 此处没法画画, 就用城市列表来表现
                self.fn打印出所有势力控制的城市列表()

                #显示操作菜单
                print("\n1. 攻击电脑")
                print("2. 结束回合")
                print("3. 退出游戏")

                # 处理玩家选择
                int玩家的菜单选中 = input("选择操作:")
                if int玩家的菜单选中 == "1": # 玩家选中要攻击电脑
                    int城市编号:int = int(input("从哪个城市起兵? 输入城市编号: "))
                    self.fn玩家发动战争(self.list电脑控制的城市实例列表[int城市编号]) # 判断战争胜负, 和战后割地赔款等操作, 已经写在这个函数里面了. 战争结束后, 会进入本while循环的下一个循环
                elif int玩家的菜单选中 == "2": # 玩家要结束本回合, 进入下一回合
                    self.fn进入下一个回合()
                elif int玩家的菜单选中 == "3": # 玩家要退出游戏
                    break # 就跳出本while 循环, 进入下一循环, 即依然在大地图模式界面, 显示菜单操作
                else:
                    print("输入菜单的编号错误")


#启动游戏
if __name__ == "__main__":  # __name__ 是当前模块名，当模块被直接运行时, 模块名为 __main__ 。这句话的意思就是，当模块被直接运行时，以下代码块将被运行，当模块是被导入时，代码块不被运行。
    ins游戏主控实例 = Cls游戏主控类()
    ins游戏主控实例.fn游戏主循环()



