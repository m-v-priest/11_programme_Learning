- [https://www.bilibili.com/video/BV1gR4y1b7oW?p=9&vd_source=52c6cb2c1143f8e222795afbab2ab1b5](https://www.bilibili.com/video/BV1gR4y1b7oW?p=18&vd_source=52c6cb2c1143f8e222795afbab2ab1b5)
-
- https://www.bilibili.com/video/BV1EK4y1b7ux?p=13&spm_id_from=pageDriver&vd_source=52c6cb2c1143f8e222795afbab2ab1b5
-
- 快捷键
	- 快速输入 Console.WriteLine() : cw+两次Tab
	- for循环：for+两次Tab
	- 快速格式化代码 : Ctrl(按住不放)+K+D
	- 移动行 : alt + 上下键
	- 复制本行到下一行上：Ctrl + D
	- 将选中行, 往下移一行位置：Alt+Shift+T
	- 删除当前行：Ctrl+Shift+L或Shift+Delete（前提是没有选中任何文本，否则Shift+Delete只删除选中的文本）
	- 注释 : ctrl+k , 然后按住ctrl不放, 再按c
	- 取消注释: ctrl+k , 然后按住ctrl不放, 再按u
	- 快速智能提示 :Ctrl+J
	-
	-
	- 选择括号、括号内的文本：Ctrl + Shift + }
	- 切换代码中的大小写:
		- 转换为大写：Ctrl + Shift + U
		- 转换为小写：Ctrl + U
		-
	-
-
- 创建项目 → 我们选"控制台应用"
  collapsed:: true
	- ![image.png](../assets/image_1673264796287_0.png)
-
- 设置
	- 修改代码显示的字体
	  collapsed:: true
		- 在工具 -> 选项里面
		- ![image.png](../assets/image_1673268052539_0.png)
	- 代码过长的话, 让它在窗口内自动换行
	  collapsed:: true
		- ![image.png](../assets/image_1673268260391_0.png)
-
- 程序的基本结构
  collapsed:: true
	- ![image.png](../assets/image_1673269557754_0.png)
- 命名空间
  collapsed:: true
	- ![image.png](../assets/image_1673270512245_0.png)
	- ```
	  ```
	- 调用另一个命名空间中的类
	  collapsed:: true
		- ```
		  namespace  S1
		  {
		      class Person { }
		  }
		  
		  namespace S2
		  {
		      Person p = new Person();   //我们想调用Person类, 但这个类, 我们是写在 S1命名空间中的, 而不在现在的 S2命名空间中. 所以无法调用, 会报错.
		  }
		  ```
-
- 输出语句
	- 基本: Console.WriteLine("Hello, World!")
	  collapsed:: true
		- ```
		  Console.WriteLine("Hello, World!");
		  Console.WriteLine(123);
		  Console.ReadLine();  // 这行用来等待用户的下一行输入. 可以防止上面的输出代码一闪而过.
		  ```
	- 输出换行: `\n`
	  collapsed:: true
		- ```
		  Console.WriteLine("1 \n 2");
		  ```
	- 输出制表符: `\t`
	- 数字加字符串, 这个操作, 会把数字自动转成字符串
	  collapsed:: true
		- ```
		  int age = 3;
		  double money = 8;
		  
		  Console.WriteLine(age+money);  //11
		  Console.WriteLine(age+"+"+money);  //3+8  ← 因为数字加字符串, 相当于都转成了字符串
		  Console.WriteLine("a+b"+age+money);  //a+b38  ← age先和前面的字符串合并, 就会先把age转成了字符串, 再把money也转成了字符串, 最终就是 不存在数字的加减了.
		  Console.WriteLine("a+b"+(age+money));  //a+b11
		  ```
-
- 变量类型
	-