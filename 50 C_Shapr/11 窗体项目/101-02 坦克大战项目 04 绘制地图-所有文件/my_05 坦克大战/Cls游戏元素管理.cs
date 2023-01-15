using my_05_坦克大战.Properties;
using System.Collections.Generic;

namespace my_05_坦克大战
{
    internal class Cls游戏元素管理
    {

        //下面创建一个列表, 用来存储你下面会批量创建出来的n个墙壁的实例.
        private static List<Cls不可移动的物体> listInsWall = new List<Cls不可移动的物体>(); // 这里的字段, 必须设为静态的, 才能被本类中的方法直接调用到.



        //创建墙壁函数(方法) 
        public static void fn创建墙壁(int xStart, int yStart, int wallCount, List<Cls不可移动的物体> listInsWall) //一个方格就是一个矩形的墙壁单位.  // wallCount : 表示要创建的墙的数量 //该"fn创建墙壁"函数, 返回一个 List<Cls不可移动的物体> 类型的东西.
        {
            int xEnd = xStart * 30;
            int yEnd = yStart * 30;

            //下面开始批量创建墙
            for (int i = yEnd; i < yEnd + wallCount * 30; i += 15) // i 其实是你新创建的墙的左上角点的x坐标.
            {
                Cls不可移动的物体 insWall1 = new Cls不可移动的物体(xEnd, i, Resources.picWall);  //可以把你导入的png图片(即 Resources.picWall), 直接作为 Image类的实例对象来用.

                Cls不可移动的物体 insWall2 = new Cls不可移动的物体(xEnd + 15, i, Resources.picWall);  //

                listInsWall.Add(insWall1); //注意, 此时listInsWall的作用, 只是把所有的墙的实例(包括它们的左上角坐标位置), 收集起来. 下面在  "fn把墙画到地图上()"方法中, 会用到这个列表.
                listInsWall.Add(insWall2);
            }
        }


        //下面的函数, 把所有创建出来的墙壁(包括它们每一块的左上角坐标位置), 收集在一个列表listInsWall中.
        public static void fn生成墙壁的列表() //
        {
            fn创建墙壁(1, 1, 5, listInsWall); // 从左上角坐标(1,1)开始, 创建5个墙
        }


        //把地图画出来的函数
        public static void fn把墙画到地图上()
        {
            foreach (var itemObj in listInsWall)  //从列表listInsWall中, 把每一个墙的实例抽取出来, 执行它们身上的"fn把本实例画到画布上()"方法.
            {
                itemObj.fn把本实例画到画布上();
            }
        }




    }
}
