using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace my_05_坦克大战
{
    internal class Cls不可移动的物体:Cls游戏元素上帝主类 //继承自"上帝类"
    {
        public Image Ins不可移动物体的图片 { get; set; }   //申明一个Image类的变量, 尚未指针指向任何实例对象.

        
        //构造方法
        public Cls不可移动的物体(int x, int y, Image ins图像实例)
        {
            this.X= x;
            this.Y= y;
            this.Ins不可移动物体的图片 = ins图像实例;
        }


        protected override Image fn获取图片实例()  //具体实现父类中定义的抽象方法
        {
            return Ins不可移动物体的图片;
        }
    }
}
