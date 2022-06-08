title:: main_numpy

- 安装 numpy
  collapsed:: true
	- 官方pip命令
	  collapsed:: true
		- pip3 install --user numpy scipy matplotlib
	- 清华源
	  collapsed:: true
		- pip3 install numpy scipy matplotlib -i https://pypi.tuna.tsinghua.edu.cn/simple
	- 国内源地址 : 在使用pip的时候加参数 -i
	  collapsed:: true
		- 清华大学：https://pypi.tuna.tsinghua.edu.cn/simple
		- 华为云：https://repo.huaweicloud.com/repository/pypi/simple
		- 阿里云：http://mirrors.aliyun.com/pypi
	- 测试是否安装成功
	  collapsed:: true
		- ```python
		  from numpy import *
		  
		  print(eye(4)) # 会输出一个4阶单位阵 
		  ```
- ndarray 数组
	- 创建 ndarray 数组 -> np.arange(num1, num2, num3, ...)
	  collapsed:: true
		- ```python
		  import numpy as np
		  
		  # 方法1:
		  a1 = np.array([1,2,3]) # 创建ndarray数组
		  print(a1) # [1 2 3]
		  print(type(a1)) # <class 'numpy.ndarray'> ndarray 就是 numpy中 的数组类型
		  
		  ---
		  
		  # 方法2:
		  a2 = np.array(range(10))
		  print(a2) # [0 1 2 3 4 5 6 7 8 9]
		  
		  ---
		  
		  # 方法3:
		  a3 = np.arange(10)
		  print(a3) # [0 1 2 3 4 5 6 7 8 9]
		  
		  a4 = np.arange(4,10,2) # 从4开始, 到不包括10, 步长为2. 
		  print(a4) # [4 6 8]
		  ```
		- 注意: np.arange()方法, 只能创建一个有终点和起点的固定步长的排列, 而不能由你自定义任意数值的矩阵. 要想自定义数值, 你只能用 np.array()方法
- 查看数据类型 -> obj.dtype
  collapsed:: true
	- ```python
	  a4 = np.arange(4,10,2) # 从4开始, 到不包括10, 步长为2
	  print(a4) # [4 6 8]
	  
	  print(a4.dtype) # int32
	  ```
- 查看数据的行列数 -> obj.shape
  collapsed:: true
	- ```python
	  a1 = np.array([[1,2,3],[4,5,6]])
	  print(a1.shape) # (2, 3) 两行三列
	  ```
- 修改数据的行列数 -> obj.reshape((新行数,新列数))
	- ```python
	  a1 = np.arange(12)
	  print(a1.shape) # (12,)
	  
	  a1 = a1.reshape((3,4)) # 进行修改, 改成3行4列
	  print(a1)
	  
	  '''
	  [[ 0  1  2  3]
	   [ 4  5  6  7]
	   [ 8  9 10 11]]
	   '''
	  
	  print(a1.shape) # (3, 4)
	  ```
	-
	- ```python
	  a1 = np.arange(24)
	  print(a1.shape) # (24,)
	  
	  a1 = a1.reshape((2,3,4)) # 改成三层嵌套, 相当于是3维空间的.
	  '''
	  改成3层列表嵌套: 
	  第一层是两个list, 
	  第二层的每个list中, 又包含3个list. 
	  第三层的每个list中, 又包含4个数值. 
	  于是就共有 2*3*4 = 24个数值.
	  '''
	  
	  print(a1)
	  
	  '''
	  [[[ 0  1  2  3]
	    [ 4  5  6  7]
	    [ 8  9 10 11]]
	  
	   [[12 13 14 15]
	    [16 17 18 19]
	    [20 21 22 23]]]
	   '''
	  
	  ---
	  
	  print(a1.shape) # (2, 3, 4)
	  
	  a1_2Dimension = a1.reshape((2,12)) # 重新改成2行12列,即二维空间中的值
	  
	  print(a1_2Dimension)
	  
	  '''
	  [[ 0  1  2  3  4  5  6  7  8  9 10 11]
	   [12 13 14 15 16 17 18 19 20 21 22 23]]
	  '''
	  
	  print(a1_2Dimension.shape) # (2, 12)
	  ```
-