# 用于加载模型和拟合评估值
import keras
import numpy as np
from keras.layers import Dense
from AI_alpha_beta import Line_Points

n = [Line_Points * Line_Points, 16, 32, 64, 24, 8, 1]  # 每层神经元的个数

class Model:
    def __init__(self):
        md = keras.Sequential()
        md.add(Dense(n[1], activation='relu', input_dim=n[0]))
        md.add(Dense(n[2], activation='relu'))
        md.add(Dense(n[3], activation='relu'))
        md.add(Dense(n[4], activation='relu'))
        md.add(Dense(n[5], activation='relu'))
        md.add(Dense(n[6], activation=None))
        # 选择想要加载的模型
        self.model = md

    def my_set_weights(self, x):
        ls = []
        sum = 0
        for i in range(6):
            ls.append(np.array(x[sum: sum + n[i] * n[i + 1]]).reshape(n[i], n[i + 1]))
            sum += n[i] * n[i + 1]
            ls.append(np.array(x[sum: sum + n[i + 1]]))
            sum += n[i + 1]
        self.model.set_weights(ls)

    # 输入当前局面，输出评估函数
    def get_score_ANN(self, board):
        x_input = np.zeros((1, Line_Points ** 2), dtype=int)
        for j in range(Line_Points):
            for i in range(Line_Points):
                x_input[0, j * Line_Points + i] = board[j][i]
        score = self.model.predict(x_input)
        return score
