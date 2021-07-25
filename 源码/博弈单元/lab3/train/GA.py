'''
通过进化算法训练评估函数（评估函数用神经网络表示）
'''
import numpy as np
import random
from two_AI_chess import *
# from two_AI_chess_UI import *

population_scale = 5  # 种群的规模
max_times = 50  # 最大进化代数
set_p = 0.001  # 突变概率

def reproduction(x, y):
    # 采用两点交叉的算法产生子代
    breakpoint1 = random.randint(0, len(x))
    breakpoint2 = random.randint(0, len(x))
    if breakpoint2 < breakpoint1:
        temp = breakpoint1
        breakpoint1 = breakpoint2
        breakpoint2 = temp
    child = np.array(list(x))
    for i in range(breakpoint1, breakpoint2 + 1):
        child[i] = y[i]
    return child


my_model = Model()
# 输出模型参数量，以便解的构建
# print(my_model.model.summary())
# print(my_model.model.count_params())

# 获得初始解
population = []
p_evaluate = []
for i in range(population_scale):
    population.append(np.random.normal(size=my_model.model.count_params()))
    p_evaluate.append([i, 0])

# 评估解的质量
# m = 0
for i in range(population_scale - 1):
    for j in range(i + 1, population_scale):
        # print("run: {}".format(m))
        # m += 1
        winner = two_AI_chess(population[i], population[j])
        if winner == 1:
            p_evaluate[i][1] += 1
            p_evaluate[j][1] -= 1
        if winner == -1:
            p_evaluate[i][1] -= 1
            p_evaluate[j][1] += 1
print("初始解已处理完毕")

# 进化部分
t = 0
while t < max_times:
    # 输出当前信息
    print("当前为第{:6}代".format(t))

    # 挑选亲代
    p_evaluate.sort(key=lambda xx: xx[1], reverse=True)
    parents_index = []
    parents_num = population_scale // 2
    for i in range(parents_num):
        parents_index.append(p_evaluate[i][0])

    # 基因交叉
    children = []
    for i in range(population_scale):
        x = random.randint(0, parents_num - 1)
        y = random.randint(0, parents_num - 1)

        while x == y:
            y = random.randint(0, parents_num - 1)
        children.append(reproduction(population[parents_index[x]],
                                     population[parents_index[y]]))

    # 基因突变
    for i in range(population_scale):
        for j in range(my_model.model.count_params()):
            if random.random() < set_p:
                children[i][j] += np.random.normal(0, 0.3)

    # 评估解的质量
    sum_scale = population_scale * 2
    s_evaluate = []
    s_population = np.concatenate((population, children), axis=0)
    for i in range(sum_scale):
        s_evaluate.append([i, 0])
    for i in range(sum_scale - 1):
        for j in range(i + 1, sum_scale):
            # 两个AI下棋得出胜者
            winner = two_AI_chess(s_population[i], s_population[j])
            if winner == 1:
                s_evaluate[i][1] += 1
                s_evaluate[j][1] -= 1
            if winner == -1:
                s_evaluate[i][1] -= 1
                s_evaluate[j][1] += 1

    # 选择下一代
    s_evaluate.sort(key=lambda x_: x_[1], reverse=True)
    print(s_evaluate)
    population = []
    for i in range(population_scale):
        population.append(s_population[s_evaluate[i][0]])
    t += 1

# 挑选排名第一的解并输出
my_model.my_set_weights(population[0])
my_model.model.save('my_solvent.h5')