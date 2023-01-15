using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace my_05_坦克大战
{
    abstract internal class Cls游戏元素上帝主类 //这里我们把它定义成"抽象类", 因为该类里面有"抽象方法"存在. 而"抽象方法"只能存在于"抽象类"中.
    {

        // 所有的元素, 都有x,y坐标属性
        public int X { get; set; }  //添加变量x, 及其属性(get,set方法). 这样, 这句的x, 就直接写成大小的X了.
        public int Y { get; set; }


        // 这里创建一个抽象方法. 因为, 对于可以动的物体, 我们需要先获取该物体的坐标位置, 才能在画布上来画它. 所以这里, 我们不能把这里面的" fn获取图片实例"函数写实, 只能让子类取完成它. 即让子类来具体实现 " fn获取图片实例"函数. 
        //因为抽象方法，必须存在于抽象类当中. 所以这里, 我们必须把本"Cls游戏元素上帝主类"也改成抽象类.
        //(不过, 抽象类中不一定全部是抽象方法, 我们可以在里面写上普通方法，有实现的虚方法或者没有实现的虚方法都可以。另外, 父类的虚方法可以实现(有方法体)，也可以不实现（没有方法体）。而抽象方法必须通过子类的重写来实现。)
        //(抽象类可以被实例化，但不能通过普通的实例化new，它只能通过父类的应用指向子类的实例来间接的实例化子类。)
        protected abstract Image fn获取图片实例(); //抽象方法


        //所有的元素, 还有共同的把自己绘制在画布上的功能
        public void fn把本实例画到画布上() 
        {
            Graphics ins画布 = Cls游戏框架.ins游戏框架中的画布; //创建一个画布类的变量, 指针指向 'Cls游戏框架类"中的画布实例.
            ins画布.DrawImage(fn获取图片实例(), X,Y); //DrawImage()方法, 接收3个参数, 第一个参数是要画在画布上的"图片实例对象". 这里会由" fn获取图片实例()"函数(方法)来得到.  X,Y 这两个参数, 就是所有物体元素都会有的坐标值. 即本"Cls游戏元素上帝主类"中定义的 X和Y两个属性的值.
        }



    }
}
