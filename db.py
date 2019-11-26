
import random;

list = [
    "序列是Python中最基本的数据结构",
    "列中的每个元素都分配一个数字",
    "序列都可以进行的操作包括索引，切片，加，乘，检查成员。",
    "Python已经内置确定序列的长度以及确定最大和最小的元素的方",
    "表的数据项不需要具有相同的类型",
    "要把逗号分隔的不同的数据项使用方括号括起来即可。如下",
    "我们使用了 random 模块的 randint() 函数来生成随机数",
    "每次执行后都返回不同的数字（0 到 9），该函数的语法为：",
]

count = list.count(list);


def getRndMsg():
    index = random.randint(0,count-1);
    return list[index];

