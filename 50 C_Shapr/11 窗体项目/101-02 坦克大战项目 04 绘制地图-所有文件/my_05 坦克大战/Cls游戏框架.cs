using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace my_05_坦克大战
{
    internal class Cls游戏框架
    {

        public static Graphics ins游戏框架中的画布; //先申明一个画布变量, 还未赋具体值(还未用指针指向具体的画布类实例对象). 这里设置成了静态属性, 就能在其他类中, 直接调用本"Cls游戏框架"类名, 来调用该画布属性了.



        //游戏开始时, 会执行的动作, 写在下面的方法里
        public static void fn游戏开始时的动作() //方法名可写成 fnStart()
        {
            Console.WriteLine("游戏开始时的动作...");
            Cls游戏元素管理.fn生成墙壁的列表();
        }



        //游戏不断更新时, 会执行的动作, 写在下面的方法里(比如, 不断重新绘制新图片, 以形成动画; 不断检测敌人的行动, 以决定玩家角色的策略). 这个就和帧率FPS有关
        public static void fn游戏不断更新时会执行的动作() //方法名可写成 fnUpdate()
        { 
            Console.WriteLine("游戏在不断更新,执行xxx动作...");
            Cls游戏元素管理.fn把墙画到地图上();
        }

    }
}
