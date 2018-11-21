# -*- coding: utf-8 -*-
# 用模拟退火算法（SA）解决指派问题
import numpy as np
import pandas as pd

n = 100  # 100个工人做100个工作

# 生成100x100的excel矩阵
writer = pd.ExcelWriter('output.xlsx')
df_random = pd.DataFrame(data=np.random.randint(1, 100, size=(n, n)))  # 生成1-100之间的随机数
df_random.to_excel(writer, 'Sheet1')
writer.save()

# 读取随机数矩阵
excel_path = 'output.xlsx'
d = pd.read_excel(excel_path)
d = np.array(d)  # 转换为数组
d_mean = np.mean(d)  # 生成的随机数的均值


# 时间函数
def total_time(arrange):
    total_time = 0  # 初始时间设为0
    for i in range(n):
        # 任务安排的形式如[2,1,4,3]表示第一个人做第二项工作，第二个人做第一项工作，第三个人做第四项工作，etc
        total_time = total_time + d[i, arrange[i]]
    return total_time


T = 200  # 设置初始温度，对应加温过程
t = 0.8  # 终止温度-> 0
alpha = 0.94  # 温度下降率，使得降温过程足够慢

now_arrange = np.random.permutation(n)  # 随机生成一个初始化安排方案
print(now_arrange)

now_time = total_time(now_arrange)  # 当前方案的消耗时间

new_arrange = now_arrange.copy()  # 新方案

best_arrange = now_arrange.copy()  # 保留历史最优安排
best_time = now_time  # 保留历史最优时间

x = 0  # 定义x计算总循环次数
y = 0  # 定义y计算外循环次数
# 外循环(温度)
while t < T:
    y = y + 1  # 外循环+1
    markov_len = int(6000 / T)  # 根据T动态设置内循环次数，随着T的减小，内循环次数增加;使用地板除取整
    for i in range(markov_len):  # (内循环，尽量保证达到热平衡)
        x = x + 1  # 内循环+1
        while True:
            k = np.random.randint(0, n, 2)  # 随机产生新解
            if k[0] != k[1]:  # 保证是两个不同的位置
                break
        new_arrange[k[0]], new_arrange[k[1]] = new_arrange[k[1]], new_arrange[k[0]]  # 交换两个位置得到新的路径
        new_time = total_time(new_arrange)  # 计算新的安排所消耗的时间
        if new_time < now_time:  # 无条件接受新解.
            now_time = new_time  # 更新时间
            now_arrange = new_arrange.copy()  # 更新安排

            if new_time < best_time:  # 更新历史最优解
                best_time = new_time
                best_arrange = new_arrange.copy()
                print(best_arrange, best_time)

        else:  # Metropolis准则：以概率接受新状态
            delta = new_time - now_time
            if np.random.rand() < np.exp(-delta / T):  # 如果Metropolis概率大于随机生成的服从0-1均匀分布的随机数则接受，
                # 但是不更新历史最优解.
                now_time = new_time
                now_arrange = new_arrange.copy()
                print(now_arrange, now_time)
            else:
                new_arrange = now_arrange.copy()  # 否则拒绝新解,维持原解.

    T = T * alpha  # 降温函数(按比例下降)

# 输出最终结果

print('外循环次数:', y)  # 输出外循环次数
print('总循环次数:', x)  # 输出总循环次数
print('dij的均值:', d_mean)  # 输出dij的均值
print('最优时间:', best_time)  # 输出最优时间
print('最优安排dij均值：', best_time / n)  # 最优安排dij均值
print('最优安排：')
for i in range(n):  # 输出最佳安排
    print(i + 1, '->', best_arrange[i] + 1, ',', end="")
