## FDSMLP 线性规划求解器！

时间有限，制作了用两阶段法完成线性规划的方法。

求解器可以输出具体的单纯形表解题步骤，做作业利器！

### 使用
#### 0 库的安装
直接pip
```
pip install FDSMLP -i https://pypi.org/project
```

#### 1 库的导入
```python
from FDSMLP.Simplex import Two_step_simplex
```

#### 2 使用
```python
A = [
    [1, 1, 2], 
    [-1 2, 1],
    [1, 0, -2]
]# 约束条件方程
b = [1, 3, -1]# 目标函数系数，数量可以比A的列数少，会自动补全为0
constrain = [4, 4, 5]# 约束条件右侧的常量
constraints =["<=","=",">="]#  约束条件方程的符号，支持不等号，会自动初始化为标准型
      
# 两阶段法求解器的初始化  
simplex=Two_step_simplex(b,A,constrain,constraints)
```
#### 3 设置单纯形表的打印风格，可以设置每一格的输出宽度
例：
```python
simplex.set_cell_width(11)
print(simplex)
```
单纯形表打印结果：
```
           |           |           |   1.000   |   3.000   |  -1.000   |   0.000   |   0.000   |   0.000   |   0.000   |
-------------------------------------------------------------------------------------------------------------------------
    CB     |    XB     |     b     |    X1     |    X2     |    X3     |    X4     |    X5     |    X6     |    X7     |
-------------------------------------------------------------------------------------------------------------------------
     0     |    X4     |   4.000   |   1.000   |   1.000   |   2.000   |   1.000   |   0.000   |   0.000   |   0.000   |
     0     |    X6     |   4.000   |  -1.000   |   2.000   |   1.000   |   0.000   |   0.000   |   1.000   |   0.000   |
     0     |    X7     |   5.000   |   1.000   |   0.000   |  -2.000   |   0.000   |  -1.000   |   0.000   |   1.000   |
-------------------------------------------------------------------------------------------------------------------------
           |           |           |   1.000   |   3.000   |   1.000   |   1.000   |  -1.000   |   0.000   |   0.000   |

-------------------------------------------------------------------------------------------------------------------------
```
```python
simplex.set_cell_width(6)
print(simplex)
```
单纯形表打印结果：
```
      |      |      |1.000 |3.000 |-1.000|0.000 |0.000 |0.000 |0.000 |
-----------------------------------------------------------------------
  CB  |  XB  |  b   |  X1  |  X2  |  X3  |  X4  |  X5  |  X6  |  X7  |
-----------------------------------------------------------------------
  0   |  X4  |4.000 |1.000 |1.000 |2.000 |1.000 |0.000 |0.000 |0.000 |
  0   |  X6  |4.000 |-1.000|2.000 |1.000 |0.000 |0.000 |1.000 |0.000 |
  0   |  X7  |5.000 |1.000 |0.000 |-2.000|0.000 |-1.000|0.000 |1.000 |
-----------------------------------------------------------------------
      |      |      |1.000 |3.000 |1.000 |1.000 |-1.000|0.000 |0.000 |

-----------------------------------------------------------------------
```

#### 4 求解
```python
from FDSMLP.Simplex import Two_step_simplex

A = [
    [0, 1, 2, 1, 0], 
    [-1, 2, 1, 1, 1],
    [3, 0, 3, 1, 0], 
]
b = [1, 3, -1]
constrain = [4, 4, 4]
constraints =["=","=","="]
simplex=Two_step_simplex(b,A,constrain,constraints)
simplex.solve()
```
输出结果:
```
开始执行两步法进行线性规划求解：
原始目标函数为：
max y = 1 * X1 + 3 * X2 - 1 * X3 - 0 * X4 - 0 * X5
原始约束条件为：
 0 * X1 + 1 * X2 + 2 * X3 + 1 * X4 + 0 * X5 = 4
 - 1 * X1 + 2 * X2 + 1 * X3 + 1 * X4 + 1 * X5 = 4
 3 * X1 + 0 * X2 + 3 * X3 + 1 * X4 + 0 * X5 = 4

进行标准化后的目标函数为：
max y = 1 * X1 + 3 * X2 - 1 * X3 - 0 * X4 - 0 * X5
标准化后得约束条件为：
 0 * X1 + 1 * X2 + 2 * X3 + 1 * X4 + 0 * X5 = 4
 - 1 * X1 + 2 * X2 + 1 * X3 + 1 * X4 + 1 * X5 = 4
 3 * X1 + 0 * X2 + 3 * X3 + 1 * X4 + 0 * X5 = 4

使用两步法修改目标函数为：
max y = 2 * X1 + 3 * X2 + 6 * X3 + 3 * X4 + 1 * X5 - 0 * X6 - 0 * X7
使用两步法修改约束条件为：
 0 * X1 + 1 * X2 + 2 * X3 + 1 * X4 + 0 * X5 + 1 * X6 + 0 * X7 = 4
 - 1 * X1 + 2 * X2 + 1 * X3 + 1 * X4 + 1 * X5 + 0 * X6 + 0 * X7 = 4
 3 * X1 + 0 * X2 + 3 * X3 + 1 * X4 + 0 * X5 + 0 * X6 + 1 * X7 = 4

初始化单纯形表后结果如下：
           |           |           |   1.000   |   3.000   |  -1.000   |   0.000   |   0.000   |   0.000   |   0.000   |
-------------------------------------------------------------------------------------------------------------------------
    CB     |    XB     |     b     |    X1     |    X2     |    X3     |    X4     |    X5     |    X6     |    X7     |
-------------------------------------------------------------------------------------------------------------------------
     0     |    X6     |   4.000   |   0.000   |   1.000   |   2.000   |   1.000   |   0.000   |   1.000   |   0.000   |
     0     |    X5     |   4.000   |  -1.000   |   2.000   |   1.000   |   1.000   |   1.000   |   0.000   |   0.000   |
     0     |    X7     |   4.000   |   3.000   |   0.000   |   3.000   |   1.000   |   0.000   |   0.000   |   1.000   |
-------------------------------------------------------------------------------------------------------------------------
           |           |           |   2.000   |   3.000   |   6.000   |   3.000   |   1.000   |   0.000   |   0.000   |

-------------------------------------------------------------------------------------------------------------------------


开始进行第一阶段运算：
           |           |           |   1.000   |   3.000   |  -1.000   |   0.000   |   0.000   |   0.000   |   0.000   |
-------------------------------------------------------------------------------------------------------------------------
    CB     |    XB     |     b     |    X1     |    X2     |    X3     |    X4     |    X5     |    X6     |    X7     |
-------------------------------------------------------------------------------------------------------------------------
     0     |    X6     |   4.000   |   0.000   |   1.000   |   2.000   |   1.000   |   0.000   |   1.000   |   0.000   |
     0     |    X5     |   4.000   |  -1.000   |   2.000   |   1.000   |   1.000   |   1.000   |   0.000   |   0.000   |
     0     |    X7     |   4.000   |   3.000   |   0.000   |   3.000   |   1.000   |   0.000   |   0.000   |   1.000   |
-------------------------------------------------------------------------------------------------------------------------
           |           |           |   2.000   |   3.000   |   6.000   |   3.000   |   1.000   |   0.000   |   0.000   |

-------------------------------------------------------------------------------------------------------------------------


以X3为入基变量，X7为出基变量进行转轴计算，得：

           |           |           |   1.000   |   3.000   |  -1.000   |   0.000   |   0.000   |   0.000   |   0.000   |
-------------------------------------------------------------------------------------------------------------------------
    CB     |    XB     |     b     |    X1     |    X2     |    X3     |    X4     |    X5     |    X6     |    X7     |
-------------------------------------------------------------------------------------------------------------------------
     0     |    X6     |   1.333   |  -2.000   |   1.000   |   0.000   |   0.333   |   0.000   |   1.000   |  -0.667   |
     0     |    X5     |   2.667   |  -2.000   |   2.000   |   0.000   |   0.667   |   1.000   |   0.000   |  -0.333   |
    -1     |    X3     |   1.333   |   1.000   |   0.000   |   1.000   |   0.333   |   0.000   |   0.000   |   0.333   |
-------------------------------------------------------------------------------------------------------------------------
           |           |           |  -4.000   |   3.000   |   0.000   |   1.000   |   1.000   |   0.000   |  -2.000   |

-------------------------------------------------------------------------------------------------------------------------


以X2为入基变量，X5为出基变量进行转轴计算，得：

           |           |           |   1.000   |   3.000   |  -1.000   |   0.000   |   0.000   |   0.000   |   0.000   |
-------------------------------------------------------------------------------------------------------------------------
    CB     |    XB     |     b     |    X1     |    X2     |    X3     |    X4     |    X5     |    X6     |    X7     |
-------------------------------------------------------------------------------------------------------------------------
     0     |    X6     |   0.000   |  -1.000   |   0.000   |   0.000   |   0.000   |  -0.500   |   1.000   |  -0.500   |
     3     |    X2     |   1.333   |  -1.000   |   1.000   |   0.000   |   0.333   |   0.500   |   0.000   |  -0.167   |
    -1     |    X3     |   1.333   |   1.000   |   0.000   |   1.000   |   0.333   |   0.000   |   0.000   |   0.333   |
-------------------------------------------------------------------------------------------------------------------------
           |           |           |  -1.000   |   0.000   |   0.000   |   0.000   |  -0.500   |   0.000   |  -1.500   |

-------------------------------------------------------------------------------------------------------------------------


第一阶段算法执行完毕，得到如上结果，此时的检验数结果为：[5.0, 0.0, 0.0, -0.6666666666666667, -1.5, 0.0, 0.8333333333333333]

人工变量X6在基变量中，进行判断
人工变量对应行的原始决策变量约束存在不为0的值，直接删除所有人工变量和基变量人工变量对应的行
           |           |           |   1.000   |   3.000   |  -1.000   |   0.000   |   0.000   |   0.000   |   0.000   |
-------------------------------------------------------------------------------------------------------------------------
    CB     |    XB     |     b     |    X1     |    X2     |    X3     |    X4     |    X5     |    X6     |    X7     |
-------------------------------------------------------------------------------------------------------------------------
     0     |    X6     |   0.000   |  -1.000   |   0.000   |   0.000   |   0.000   |  -0.500   |   1.000   |  -0.500   |
     3     |    X2     |   1.333   |  -1.000   |   1.000   |   0.000   |   0.333   |   0.500   |   0.000   |  -0.167   |
    -1     |    X3     |   1.333   |   1.000   |   0.000   |   1.000   |   0.333   |   0.000   |   0.000   |   0.333   |
-------------------------------------------------------------------------------------------------------------------------
           |           |           |   5.000   |   0.000   |   0.000   |  -0.667   |  -1.500   |   0.000   |   0.833   |

-------------------------------------------------------------------------------------------------------------------------


以X1为入基变量，X6为出基变量进行转轴计算，得：

           |           |           |   1.000   |   3.000   |  -1.000   |   0.000   |   0.000   |   0.000   |   0.000   |
-------------------------------------------------------------------------------------------------------------------------
    CB     |    XB     |     b     |    X1     |    X2     |    X3     |    X4     |    X5     |    X6     |    X7     |
-------------------------------------------------------------------------------------------------------------------------
     1     |    X1     |  -0.000   |   1.000   |  -0.000   |  -0.000   |  -0.000   |   0.500   |  -1.000   |   0.500   |
     3     |    X2     |   1.333   |   0.000   |   1.000   |   0.000   |   0.333   |   1.000   |  -1.000   |   0.333   |
    -1     |    X3     |   1.333   |   0.000   |   0.000   |   1.000   |   0.333   |  -0.500   |   1.000   |  -0.167   |
-------------------------------------------------------------------------------------------------------------------------
           |           |           |   0.000   |   0.000   |   0.000   |  -0.667   |  -4.000   |   5.000   |  -1.667   |

-------------------------------------------------------------------------------------------------------------------------


以X5为入基变量，X1为出基变量进行转轴计算，得：

           |           |           |   1.000   |   3.000   |  -1.000   |   0.000   |   0.000   |   0.000   |   0.000   |
-------------------------------------------------------------------------------------------------------------------------
    CB     |    XB     |     b     |    X1     |    X2     |    X3     |    X4     |    X5     |    X6     |    X7     |
-------------------------------------------------------------------------------------------------------------------------
     0     |    X5     |  -0.000   |   2.000   |  -0.000   |  -0.000   |  -0.000   |   1.000   |  -2.000   |   1.000   |
     3     |    X2     |   1.333   |  -2.000   |   1.000   |   0.000   |   0.333   |   0.000   |   1.000   |  -0.667   |
    -1     |    X3     |   1.333   |   1.000   |   0.000   |   1.000   |   0.333   |   0.000   |   0.000   |   0.333   |
-------------------------------------------------------------------------------------------------------------------------
           |           |           |   8.000   |   0.000   |   0.000   |  -0.667   |   0.000   |  -3.000   |   2.333   |

-------------------------------------------------------------------------------------------------------------------------


最终单纯形表为：
           |           |           |   1.000   |   3.000   |  -1.000   |   0.000   |   0.000   |
-------------------------------------------------------------------------------------------------
    CB     |    XB     |     b     |    X1     |    X2     |    X3     |    X4     |    X5     |
-------------------------------------------------------------------------------------------------
     0     |    X5     |  -0.000   |   2.000   |  -0.000   |  -0.000   |  -0.000   |   1.000   |
     3     |    X2     |   1.333   |  -2.000   |   1.000   |   0.000   |   0.333   |   0.000   |
    -1     |    X3     |   1.333   |   1.000   |   0.000   |   1.000   |   0.333   |   0.000   |
-------------------------------------------------------------------------------------------------
           |           |           |   8.000   |   0.000   |   0.000   |  -0.667   |   0.000   |

-------------------------------------------------------------------------------------------------


[0, 1.3333333333333335, 1.3333333333333333, 0, -0.0]
线性规划解得最优解为：[0, 1.3333333333333335, 1.3333333333333333, 0, -0.0],此时目标函数极大值为：2.666666666666667
```
在实际终端中运行，每次转轴的变量都会标红显示

#### 5 内置的parse_input函数使用
```python
from FDSMLP.core.utils.input_parser import parse_input
from FDSMLP.Simplex import Two_step_simplex


constrain,A,b,constraints=parse_input()

simplex=Two_step_simplex(b,A,constrain,constraints)
simplex.solve()
```


输出结果如下：
```
请输入目标函数的系数，用空格分隔: 1 3 -1
请输入约束条件（例如 '1 2 <= 3'），输入 'end' 或直接回车结束输入: 1 1 2 <= 4
请输入约束条件（例如 '1 2 <= 3'），输入 'end' 或直接回车结束输入: -1 2 1 <= 4
请输入约束条件（例如 '1 2 <= 3'），输入 'end' 或直接回车结束输入: 
开始执行两步法进行线性规划求解：
原始目标函数为：
max y = 1.0 * X1 + 3.0 * X2 - 1.0 * X3
原始约束条件为：
 1.0 * X1 + 1.0 * X2 + 2.0 * X3 <= 4.0
 - 1.0 * X1 + 2.0 * X2 + 1.0 * X3 <= 4.0
 ...
 ```

 ### 说明
 该项目目前不依赖第三方库，只依赖于python内置模块
 其实做的时候就后悔了，但是写都写了，懒得改了，反正大家也就拿来图一乐

