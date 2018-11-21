#遗传算法解决欺骗性问题
import numpy as np
import math
from matplotlib import pyplot as plt

DNA_size = 100  # DNA长度
population_size = 400  # 种群大小
cross_rate = 0.85  # 交叉率
mutation_rate = 0.0005  # 变异率
iter_N = 180  # 迭代270次
population_value = []  # 适应值数组，用来装适应值
child_new = []

population = np.random.randint(2, size=(population_size, DNA_size))  # 初始化种群DNA,小于2表示数值为0或1。大小为400x100的矩阵
np.set_printoptions(threshold=np.inf)


def translation(population):  # 翻译DNA
    for i in range(population_size):
        sum = 0  # 归0
        for j in range(25):
            x_bits = list(population[i][4 * j:4 * (j + 1)])
            if (x_bits == [0, 0, 0, 0]):
                sum = sum + 28
            elif (x_bits == [0, 0, 0, 1]):
                sum = sum + 26
            elif (x_bits == [0, 0, 1, 0]):
                sum = sum + 24
            elif (x_bits == [0, 0, 1, 1]):
                sum = sum + 18
            elif (x_bits == [0, 1, 0, 0]):
                sum = sum + 22
            elif (x_bits == [0, 1, 0, 1]):
                sum = sum + 6
            elif (x_bits == [0, 1, 1, 0]):
                sum = sum + 14
            elif (x_bits == [0, 1, 1, 1]):
                sum = sum + 0
            elif (x_bits == [1, 0, 0, 0]):
                sum = sum + 20
            elif (x_bits == [1, 0, 0, 1]):
                sum = sum + 12
            elif (x_bits == [1, 0, 1, 0]):
                sum = sum + 10
            elif (x_bits == [1, 0, 1, 1]):
                sum = sum + 2
            elif (x_bits == [1, 1, 0, 0]):
                sum = sum + 8
            elif (x_bits == [1, 1, 0, 1]):
                sum = sum + 4
            elif (x_bits == [1, 1, 1, 0]):
                sum = sum + 6
            elif (x_bits == [1, 1, 1, 1]):
                sum = sum + 30

        population_value.append(sum)

    return population_value


def select(population, fitness):  # 自然选择，选择适应值比较大的进行交叉

    index = np.random.choice(np.arange(population_size), size=population_size, replace=True,
                             p=fitness / fitness.sum())  # 轮盘赌的方式选择
    return population[index]


def crossover(parent, person):  # 交叉
    if np.random.rand() < cross_rate:
        i = np.random.randint(0, population_size, size=1)  # 随机选择另一个个体进行交叉
        cross_points1 = int(np.random.randint(0, DNA_size, size=1))  # 随机选择交叉点、双点交叉
        cross_points2 = int(np.random.randint(0, DNA_size, size=1))  # 随机选择交叉点、双点交叉
        if (cross_points1 < cross_points2):
            parent[cross_points2 - cross_points1:DNA_size - cross_points1] = person[i, cross_points2:]  # 交叉
        else:
            parent[cross_points1 - cross_points2:DNA_size - cross_points2] = person[i, cross_points1:]  # 交叉

    return parent


def mutate(child):  # 变异
    for point in range(DNA_size):
        if np.random.rand() < mutation_rate:
            child[point] = 1 if child[point] == 0 else 0
    return child


# 计算交叉变异后子代的值
def child_value(population):  # 翻译DNA
    sum = 0  # 归0
    for j in range(25):
        y_bits = list(population[4 * j:4 * (j + 1)])
        if (y_bits == [0, 0, 0, 0]):
            sum = sum + 28
        elif (y_bits == [0, 0, 0, 1]):
            sum = sum + 26
        elif (y_bits == [0, 0, 1, 0]):
            sum = sum + 24
        elif (y_bits == [0, 0, 1, 1]):
            sum = sum + 18
        elif (y_bits == [0, 1, 0, 0]):
            sum = sum + 22
        elif (y_bits == [0, 1, 0, 1]):
            sum = sum + 6
        elif (y_bits == [0, 1, 1, 0]):
            sum = sum + 14
        elif (y_bits == [0, 1, 1, 1]):
            sum = sum + 0
        elif (y_bits == [1, 0, 0, 0]):
            sum = sum + 20
        elif (y_bits == [1, 0, 0, 1]):
            sum = sum + 12
        elif (y_bits == [1, 0, 1, 0]):
            sum = sum + 10
        elif (y_bits == [1, 0, 1, 1]):
            sum = sum + 2
        elif (y_bits == [1, 1, 0, 0]):
            sum = sum + 8
        elif (y_bits == [1, 1, 0, 1]):
            sum = sum + 4
        elif (y_bits == [1, 1, 1, 0]):
            sum = sum + 6
        elif (y_bits == [1, 1, 1, 1]):
            sum = sum + 30

    return sum


def scatt(j):
    # 散点图，数据可视化
    plt.figure()  # 画布
    # s表示点点的大小，c是color嘛，marker就是点点的形状o,x,*><^,都可以啦
    # alpha是点点的亮度，label是标签啦
    plt.scatter(np.arange(population_size), values_new, s=10, c='green', marker='o', alpha=0.7)
    plt.title("fitness-sactter " + str(j + 1))
    plt.xlabel("person")
    plt.ylabel("fitness")
    # plt.legend(loc='upper right')  # 右上角标签

    plt.show()  # 显示图像


# 主函数
for j in range(iter_N):
    F_values = translation(population)  # 计算适应值对应的值

    population = select(population, np.array(F_values))  # 选择
    pop_copy = population.copy()

    for parent in population:  # 对种群中的每个个体都进行交叉变异
        child = crossover(parent, population)  # 交叉
        child = mutate(child)  # 变异

        ch = child_value(child)
        if (ch > np.median(F_values)):  # 子代适应值超过中位数则接受
            pop_copy[np.argmin(F_values), :] = child  # 将原种群中的适应值最小的一个替换掉
            F_values[np.argmin(F_values)] = ch  # 更新适应值

    population = pop_copy.copy()  # 将跟新后的种群重新给population

    population_value.clear()  # 清空适应值，非常重要，浅复制
    values_new = translation(pop_copy)  # 计算新的值
    x = np.argmax(values_new)  # 找出最大值所在的位置argmax返回数值最大数的下标
    print("Most fitted DNA: ", population[x])  # 输出最大值对应的基因
    print("适应值: ", values_new[x])  # 输出最大适应值

    scatt(j)  # 画散点图，数据可视化
    population_value.clear()  # 清空适应值，进行下一次迭代
