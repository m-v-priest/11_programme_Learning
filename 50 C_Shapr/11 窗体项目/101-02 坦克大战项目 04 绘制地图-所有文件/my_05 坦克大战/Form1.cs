using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace my_05_坦克大战
{
    public partial class Form1 : Form
    {
        private Thread t线程1; // 先申明一个 Thread类的变量
        private Graphics ins画布;  //申明画布变量


        //下面是本Form1类的"构造函数"
        public Form1()
        {
            InitializeComponent();

            //窗口居中显示
            this.StartPosition = FormStartPosition.CenterScreen;

            //创建画布实例
            ins画布 = this.CreateGraphics();
            Cls游戏框架.ins游戏框架中的画布 = ins画布; //将本Form1类中创建的画布实例, 让"Cls游戏框架"类中的画布实例, 来指针指向它.



            //我们创建一个线程. 来运行游戏的主内容. 为什么要创建新线程来运行它? 因为这样就不会阻塞我们对本Form1类(比如构造方法)等的运行了.
            //注意, 这个代码是写在 Form1.cs 文件中的.
            t线程1 = new Thread(new ThreadStart(fn游戏主线程));
            t线程1.Start();

        }

        //创建一个静态方法. 就可以直接用类名来调用它了, 而不需要创建出实例对象再来调用.
        private static void fn游戏主线程() //注意, 这里是"游戏逻辑"的主线程, 而不是整个"坦克大战"项目的主线程. 后者是写在Main函数里的. 换言之, 这里的 "fn游戏主线程", 只是在 "Main函数"主线程下, 创建出的一个子线程而已.  子线程不结束, 一直在运行的话, 主线程也不会被结束.
        {
            Cls游戏框架.fn游戏开始时的动作(); //我们来调用另一个类"Cls游戏框架"中的静态方法. 直接用类名来调用.


            int time帧率睡眠 = 1000 / 60;   //我们不需要让游戏毫秒级更新, 只需让它达到60帧就行了, 即1/60秒内, 更新一次. 我们先在这里设置好这个"cpu睡眠时间", 下面会用到

            //下面,就持续不断地来执行"更新函数"会做的动作
            while (true)
            {
                Cls游戏框架.ins游戏框架中的画布.Clear(Color.Black); // Clear()方法, 用来用某个颜色清空画布

                Cls游戏框架.fn游戏不断更新时会执行的动作();
                Thread.Sleep(time帧率睡眠);
            }
        }


        //下面这个, 就是针对 FormClosed事件, 会执行的方法函数.
        private void Form1_FormClosed(object sender, FormClosedEventArgs e)
        {
            t线程1.Abort();  //即, 一旦监测到窗体被关闭了, 我们也让游戏线程关闭.
        }
    }
}
