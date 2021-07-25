# 用于加载模型和拟合评估值
from keras.models import load_model
import numpy as np
from AI_alpha_beta import Line_Points

class Model:
    def __init__(self):
        # 选择想要加载的模型
        self.model = load_model('my_solvent.h5', compile=False)

    # 输入当前局面，输出评估函数
    def get_score_ANN(self, board):
        x_input = np.zeros((1, Line_Points ** 2), dtype=int)
        for j in range(Line_Points):
            for i in range(Line_Points):
                x_input[0, j * Line_Points + i] = board[j][i]
        score = self.model.predict(x_input)
        return score