

import random
from dataclasses import dataclass
from enum import Enum, auto

#界面状态切换类
class ClsEnum界面模式(Enum):
    enum大地图模式 = auto()
    enum内政界面模式 =auto() # 从政府内政界面, 来管理所有城市
    enum战争模式 = auto()


#各势力名字, 枚举类
class ClsEnum各政治势力名字(Enum):
    enum蜀 = "蜀"
    enum魏 = "魏"
    enum吴 = "吴"

#由玩家还是电脑控制, 枚举类
class ClsEnum玩家还是电脑(Enum):
    enum玩家 = "玩家"
    enum电脑 = "电脑"


#人才类
@dataclass
class Cls人才类:
    str人才名字:str
    enum所属政治势力:ClsEnum各政治势力名字
    int政治能力: int #决定治国能力
    int统帅能力:int #决定战争能力

    def fn治国(self):
        print(f"{self.str人才名字}在治国")

    def fn思考是否发动战争(self):
        print(f"{self.str人才名字}在思考是否发动战争")

#城市类
@dataclass
class Cls城市类:
    str城市名 :str
    enum本城所属势力:ClsEnum各政治势力名字
    enum玩家还是电脑控制: ClsEnum玩家还是电脑
    list人才实例列表 : list[Cls人才类] = None # 这里不能直接写 list() 或 [] 来赋值空列表, 会报错:  Mutable default 'list()' is not allowed. Use 'default_factory'

    # 下面的方法, 会在本类初始化时, 被自动执行
    def __post_init__(self):
        self.list人才实例列表 = self.list人才实例列表 or [] # 如果用户在实例化本类时, 传入了人才实例列表, 就用这个列表. 否则, 就用空列表来赋值.


# 先创建存放所有人才的一个数据库. 这个人才列表数据库, 应该用dict来表示, 可以修改里面的值, 否则, 人才的跳槽, 没法修改所属势力.
list所有人才实例列表 :[Cls人才类]= [
    Cls人才类("曹操", ClsEnum各政治势力名字.enum魏, 10, 9), # 姓名, 所属政治势力, 政治能力, 统帅能力
    Cls人才类("张辽", ClsEnum各政治势力名字.enum魏, 6, 8),
    Cls人才类("诸葛亮",ClsEnum各政治势力名字.enum蜀 ,10, 9),
    Cls人才类("刘备",ClsEnum各政治势力名字.enum蜀 ,8,6),
    Cls人才类("关羽",ClsEnum各政治势力名字.enum蜀, 6,8),
    Cls人才类("孙权",ClsEnum各政治势力名字.enum吴,8,4),
    Cls人才类("周瑜",ClsEnum各政治势力名字.enum吴,8,8),
]


list魏国人才实例列表 : list[Cls人才类] = []
list蜀国人才实例列表 : list[Cls人才类] = []
list吴国人才实例列表 : list[Cls人才类] = []

#下面, 我们来根据所属势力,来吧上面的各国人才空列表, 来填充进人才进去. 这是人才数据库的默认状态, 而非有跳槽的情况.
for ins人才实例 in list所有人才实例列表:
    match ins人才实例.enum所属政治势力:
        case ClsEnum各政治势力名字.enum魏:
            list魏国人才实例列表.append(ins人才实例)
        case  ClsEnum各政治势力名字.enum蜀:
            list蜀国人才实例列表.append(ins人才实例)
        case ClsEnum各政治势力名字.enum吴:
            list吴国人才实例列表.append(ins人才实例)

# 创建存放所有城市实例的一个数据库
list所有城市实例列表:[Cls城市类] = [
    Cls城市类("许昌",ClsEnum玩家还是电脑.enum电脑,list魏国人才实例列表),
    Cls城市类("成都",ClsEnum玩家还是电脑.enum玩家,list蜀国人才实例列表),
    Cls城市类("建业",ClsEnum玩家还是电脑.enum电脑,list吴国人才实例列表),
]



#游戏主控类
class Cls游戏主控类:
    def __init__(self): # 在这里, 我们进行游戏中相关数据的初始化赋值
        self.bool是否继续游戏 = True # 使用一个 "self.bool是否继续游戏" 的标志变量，来控制 最后的 "主控循环函数"中的 while 循环是否继续。 你也可以用 sys.exit() 来直接终止程序，不过推荐使用 bool 控制，便于将来加入“存档提示”“确认退出”等功能。
        self.enum界面模式 = ClsEnum界面模式.enum大地图模式 #刚进游戏时,先进入大地图模式界面的状态
        self.enum玩家所选的势力: ClsEnum各政治势力名字
        self.list所有人才实例列表 :[Cls人才类]= list所有人才实例列表 # 从外面拿到整个人才列表, 相当于导入了人才数据库, 只不过放在一个列表中, 但更好的选中, 是放在dict中
        self.list所有城市实例列表:[Cls城市类] = list所有城市实例列表 # 从外面拿到整个城市列表, 相当于导入了城市数据库, 只不过放在一个列表中

    def fn显示所有城市信息(self):
        print("三国所有城市信息:\n")
        for intIndex,ins城市实例 in enumerate(self.list所有城市实例列表):
            print(f"{intIndex}: {ins城市实例.str城市名} /  {ins城市实例.enum本城所属势力.value} / {ins城市实例.enum玩家还是电脑控制}")

    def fn显示所有人才信息(self):
        print("三国所有人才信息:\n")
        for intIndex, ins人才实例 in enumerate(self.list所有人才实例列表):
            print(f"{intIndex} :  {ins人才实例.enum所属政治势力} / {ins人才实例.str人才名字} / 政治能力: {ins人才实例.int政治能力} / 统帅能力: {ins人才实例.int统帅能力}")

    # 下面的函数,专门用来打印属于某一政治实例的人才列表
    def fn打印某一政治势力的人才列表(self, enum势力名: ClsEnum各政治势力名字):  # 传入势力名字. 注意!! 类中的方法, 第一个参数必须是self, 不要忘记写! 否则会报错.
        for intIndex, ins人才实例 in enumerate(list所有人才实例列表):
            if ins人才实例.enum所属政治势力 == enum势力名:
                print(
                    f"{intIndex} :  {ins人才实例.enum所属政治势力} / {ins人才实例.str人才名字} / 政治能力: {ins人才实例.int政治能力} / 统帅能力: {ins人才实例.int统帅能力}")

    # 下面的函数,专门用来打印属于某一政治实例的城市列表
    def fn打印某一政治势力的城市列表(enum势力名: ClsEnum各政治势力名字):  # 传入势力名字
        pass

    def fn人事任免(self):
        print("----> 正在进行人事任免")

    def fn让政府人员都去各司其职(self):
        print("----> 已经让政府人员都去各司其职")

    def fn发动战争(self):
        print("----> 发动战争操作...")




    def fn主界面模式下的菜单操作(self):
        self.fn显示所有城市信息()
        # 下面是要用户游戏时, 选择的菜单
        print("选择要扮演的势力: 1.魏, 2.蜀, 3.吴")
        print("4.退出游戏")

        int玩家选中的菜单编号 = int(input("选择编号:"))
        match int玩家选中的菜单编号:
            case 1:
                self.enum界面模式 = ClsEnum界面模式.enum内政界面模式
                self.enum玩家所选的势力 = ClsEnum各政治势力名字.enum魏
                self.fn内政界面模式下的菜单操作()
            case 2:
                self.enum界面模式 = ClsEnum界面模式.enum内政界面模式
                self.enum玩家所选的势力 = ClsEnum各政治势力名字.enum蜀
                self.fn内政界面模式下的菜单操作()
            case 3:
                self.enum界面模式 = ClsEnum界面模式.enum内政界面模式
                self.enum玩家所选的势力 = ClsEnum各政治势力名字.enum吴
                self.fn内政界面模式下的菜单操作()
            case 4:
                print("----> 你选择了退出游戏")
                self.bool是否继续游戏 = False

    def fn内政界面模式下的菜单操作(self):
        print(f"----> 你现在进入了内政模式界面, 你所控制的势力是:{self.enum玩家所选的势力.value}")

        # 下面是要用户游戏时, 选择的菜单
        print("1.人事任免")
        print("2.让政府人员都去各司其职")
        print("3.显示本势力的人才列表")
        print("4.发动战争")
        print("5.结束本回合, 进入下一回合")
        print("6.退出游戏")

        int玩家选中的菜单编号 = int(input("选择编号:"))
        match int玩家选中的菜单编号:
            case 1:
                self.fn人事任免()
            case 2:
                self.fn让政府人员都去各司其职()
            case 3:
                self.fn打印某一政治势力的人才列表(self.enum玩家所选的势力)
            case 4:
                self.fn发动战争()
            case 5:
                print("----> 你选择了进入下一回合")
            case 6:
                print("----> 你选择了退出游戏")
                self.bool是否继续游戏 = False
    def fn主控循环(self):
        #游戏主循环
        while self.bool是否继续游戏 == True:
            match self.enum界面模式 :
                case ClsEnum界面模式.enum大地图模式:
                    self.fn主界面模式下的菜单操作()
                case ClsEnum界面模式.enum内政界面模式:
                    self.fn内政界面模式下的菜单操作()


# 启动游戏
if __name__ == "__main__":
    ins主控实例 = Cls游戏主控类()
    ins主控实例.fn主控循环()

