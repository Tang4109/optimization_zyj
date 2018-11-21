city_number = 5  # 城市总数
table_length = 3  # 禁忌表长度
taboo_table = [] #禁忌表

# ==========================================
# 两个城市之间的距离矩阵
distance_matrix=[[0, 10, 15, 6, 2], [10, 0, 8, 13, 9], [15, 8, 0, 20, 15], [6, 13, 20, 0, 5], [2, 9, 15, 5, 0]]

# 计算领域解中所有路径对应的距离
def cal_path(distance_matrix, path):
    dis_list = []
    for each in path:
        dis = 0
        for j in range(city_number - 1):
            dis = distance_matrix[each[j]][each[j + 1]] + dis
        dis = distance_matrix[each[4]][each[0]] + dis  # 回家
        dis_list.append(dis)
    return dis_list
# 寻找上一个最优路径对应的所有领域解.
def find_path(path_best):
    path_new = []
    for i in range(city_number - 1):
        for j in range(i + 1, city_number):
            path = path_best.copy() #复制
            path[i], path[j] = path[j], path[i] #2-opt
            path_new.append(path)
    return path_new


# ==========================================
# 设置初始解
path_initial = []
firstValue = [1,4,3,2,5] #初始解为1,2,3,4,5
list = [x - 1 for x in firstValue] #Python中转为0,1,2,3,4
initial = list
path_initial.append(initial)

# 加入禁忌表
#将移动后的结果放入禁忌表，等同于将移动放入禁忌表
taboo_table.append(initial)

# 求初始解的路径长度
dis_list = cal_path(distance_matrix, path_initial)
dis_best = min(dis_list)  # 最短距离
path_best = path_initial[dis_list.index(dis_best)]  # 对应的最短路径方案

# 初始渴望
expect_dis = dis_best
expect_path = path_best
print('禁忌表迭代过程：')
for iter in range(5):  # 迭代5次
    # 寻找新的领域解
    path_new = find_path(path_best)
    # 求出所有新解的路径长度
    dis_new = cal_path(distance_matrix, path_new)
    # 选择新的最短路径
    dis_best = min(dis_new)  # 最短距离
    path_best = path_new[dis_new.index(dis_best)]  # 对应的最短路径方案
    if dis_best < expect_dis:  # 最短的路径如果小于期望
        expect_dis = dis_best
        expect_path = path_best  # 更新两个渴望（可以冲破渴望水平）
        if path_best in taboo_table:
            taboo_table.remove(path_best)
            taboo_table.append(path_best)
        else:
            taboo_table.append(path_best) #更新禁忌表
    else:  # 如果最短路径的还是不能改善历史最优值
        #以次优解代替最优解，for循环观察禁忌表中的每个元素，保证次优解不在禁忌表中
        for i in range(table_length):
            if path_best in taboo_table:  # 如果在禁忌表里，则移除
                dis_new.remove(dis_best)
                path_new.remove(path_best)
                dis_best = min(dis_new)  # 求新的次优解
                path_best = path_new[dis_new.index(dis_best)]  # 对应新次优解的最短路径方案
        taboo_table.append(path_best)# 不在禁忌表中则选中
        #超过禁忌表规定长度则把先进入禁忌表的数据踢出
        if len(taboo_table) > table_length:
                del taboo_table[0]
    #tab = [x + 1 for x in taboo_table]
    print(taboo_table)
lis = [x + 1 for x in list]
#lis.append(lis[0])
print('初始解：',lis)
print('最短距离', expect_dis)
result = [x + 1 for x in expect_path]
#result.append(result[0])
print('最短路径：', result)

