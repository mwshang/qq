
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


# 聊天话题
chat_topics = [
    "无聊",
    "网恋算是真正的恋爱吗",
    "做过春梦吧?说说看",
    "婚后会要孩子吗",
    "你会如何培养孩子的道德价值观",
    "你喜欢什么动物，不喜欢什么",
    "当你对某人有偏见时，你是怎么想的",
    "如果你中了彩票，还会继续上班吗",
    "你现在最想去哪儿?为什么?",
    "希望改变自己的什么?",
    "你最害怕什么?",
    "你认为谎言有度吗?",
]
chat_topics_count = len(chat_topics);


def getRndMsg():
    index = random.randint(0,count-1);
    return list[index];

def GetRndTopicMsg():
    index = random.randint(0,chat_topics_count-1);
    return chat_topics[index];

