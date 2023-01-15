using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace my_05_坦克大战
{

    //定义一个枚举类型, 用来表示"朝向"的4个方位
    enum Enm朝向
    {
        Up, Down, Left, Right
    }

    internal class Cls可以动的物体 : Cls游戏元素上帝主类
    {
        //因为可移动物体, 需要四张图来分布显示它们的: 向上, 向下,向左, 向右 的样子.所以我们这里创建4个 Image对象 (或 Bitmap对象也可以).
        public Bitmap Ins可移动物体的up图片 { get; set; }
        public Bitmap Ins可移动物体的down图片 { get; set; }
        public Bitmap Ins可移动物体的left图片 { get; set; }
        public Bitmap Ins可移动物体的right图片 { get; set; }


        //可移动物体, 还有"朝向"属性, 它到底是面向东西南北哪个方向?
        public Enm朝向 Ins枚举朝向 { get; set; }  //创建一个"朝向"枚举类的变量


        //速度属性
        public int Ins速度 { get; set; }


        //具体实现父类中定义的抽象方法
        protected override Image fn获取图片实例()
        {
            switch (Ins枚举朝向)
            {
                case Enm朝向.Up:
                    return Ins可移动物体的up图片;
                case Enm朝向.Down:
                    return Ins可移动物体的down图片;
                case Enm朝向.Left:
                    return Ins可移动物体的left图片;
                case Enm朝向.Right:
                    return Ins可移动物体的right图片;
            }

            return Ins可移动物体的up图片; //如果上面的switch中的条件都不满足,就返回"Ins可移动物体的up图片". 这句代码一定要写, 否则vs会默认你 switch没有 如同"有if 却没有 else功能"的语句, 而报错.
        }


    }
}
