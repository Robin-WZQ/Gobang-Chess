'''alpha-beta剪枝'''

# AI搜索的深度
AI_SEARCH_DEPTH = 2  # 定义AI搜索的深度,深度2是最佳的
from enum import IntEnum
import time
from collections import namedtuple

Line_Points = 9  # 每行的点数

class CHESS_TYPE(IntEnum):
    NONE = 0,
    SLEEP_TWO = 1,
    LIVE_TWO = 2,
    SLEEP_THREE = 3
    LIVE_THREE = 4,
    CHONG_FOUR = 5,
    LIVE_FOUR = 6,
    LIVE_FIVE = 7,


CHESS_TYPE_NUM = 8

FIVE = CHESS_TYPE.LIVE_FIVE.value
FOUR, THREE, TWO = CHESS_TYPE.LIVE_FOUR.value, CHESS_TYPE.LIVE_THREE.value, CHESS_TYPE.LIVE_TWO.value
SFOUR, STHREE, STWO = CHESS_TYPE.CHONG_FOUR.value, CHESS_TYPE.SLEEP_THREE.value, CHESS_TYPE.SLEEP_TWO.value

offset = [(1, 0), (0, 1), (1, 1), (1, -1)]
Chessman = namedtuple('Chessman', 'Name Value Color')
Point = namedtuple('Point', 'X Y')
BLACK_CHESSMAN = Chessman('黑子', 1, (45, 45, 45))
WHITE_CHESSMAN = Chessman('白子', 2, (255, 255, 255))

CHESS_TYPE_NUM = 8

FIVE = CHESS_TYPE.LIVE_FIVE.value
FOUR, THREE, TWO = CHESS_TYPE.LIVE_FOUR.value, CHESS_TYPE.LIVE_THREE.value, CHESS_TYPE.LIVE_TWO.value
SFOUR, STHREE, STWO = CHESS_TYPE.CHONG_FOUR.value, CHESS_TYPE.SLEEP_THREE.value, CHESS_TYPE.SLEEP_TWO.value

SCORE_MAX = 0x7fffffff
SCORE_MIN = -1 * SCORE_MAX


# SCORE_FIVE = 10000


class ChessAI():
    def __init__(self, line_points, chessman):
        self.len = line_points  # 10
        self._my = chessman
        # 水平、竖直、左右斜方向
        self.record = [[[0, 0, 0, 0] for x in range(line_points)] for y in range(line_points)]
        self.count = [[0 for x in range(CHESS_TYPE_NUM)] for i in range(2)]
        self.pos_score = [[(9 - max(abs(x - 9), abs(y - 9))) for x in range(line_points)] for y in range(line_points)]
        self._opponent = BLACK_CHESSMAN if chessman == WHITE_CHESSMAN else WHITE_CHESSMAN
        # 单纯循环整个棋盘
        self.board = [[0] * line_points for _ in range(line_points)]

    def reset(self):
        for y in range(self.len):
            for x in range(self.len):
                for i in range(4):
                    self.record[y][x][i] = 0

        for i in range(len(self.count)):
            for j in range(len(self.count[0])):
                self.count[i][j] = 0

    # 获得对手的棋，也就是电脑玩家鼠标点击的地方
    def get_opponent_drop(self, point):
        self.board[point.Y][point.X] = self._opponent.Value  # 1

    def click(self, map, x, y, turn):
        map.click(x, y, turn)

    # check if has a none empty position in it's radius range
    def hasNeighbor(self, x, y, radius):
        start_x, end_x = (x - radius), (x + radius)
        start_y, end_y = (y - radius), (y + radius)

        for i in range(start_y, end_y + 1):
            for j in range(start_x, end_x + 1):
                if i >= 0 and i < self.len and j >= 0 and j < self.len:
                    if self.board[i][j] != 0:
                        return True
        return False

    # get all positions near chess
    def genmove(self, turn):
        fives = []
        mfours, ofours = [], []
        msfours, osfours = [], []
        if turn == WHITE_CHESSMAN.Value:
            mine = 2
            opponent = 1
        else:
            mine = 1
            opponent = 2

        moves = []
        radius = 1

        for y in range(self.len):  # self.len=10
            for x in range(self.len):
                if self.board[y][x] == 0 and self.hasNeighbor(x, y, radius):  # hasNeignbor查看周围是否有棋子
                    score = self.pos_score[y][x]
                    moves.append((score, x, y))

        moves.sort(reverse=True)
        return moves

    def __search(self, AI_model, turn, depth, alpha=SCORE_MIN, beta=SCORE_MAX):
        # 用模型预测的值作为评估函数
        score = AI_model.get_score_ANN(self.board)
        # if depth <= 0 or abs(score) >= SCORE_FIVE:
        if depth <= 0:
            return score

        moves = self.genmove(turn)
        bestmove = None
        self.alpha += len(moves)

        # if there are no moves, just return the score
        if len(moves) == 0:
            return score

        for _, x, y in moves:
            self.board[y][x] = turn
            if turn == WHITE_CHESSMAN.Value:
                op_turn = BLACK_CHESSMAN.Value
            else:
                op_turn = WHITE_CHESSMAN.Value

            score = - self.__search(AI_model, op_turn, depth - 1, -beta, -alpha)

            self.board[y][x] = 0
            self.belta += 1

            # alpha/beta pruning
            if score > alpha:
                alpha = score
                bestmove = (x, y)
                if alpha >= beta:
                    break

        if depth == self.maxdepth and bestmove:
            self.bestmove = bestmove
        return alpha

    def search(self, turn, depth, AI_model):
        self.maxdepth = depth
        self.bestmove = None
        score = self.__search(AI_model, turn, depth)
        # 找不到最佳的位置则返回(-1, -1)
        if self.bestmove == None:
            # 如果没有最好的点，则随机给一个
            for y in range(Line_Points):
                for x in range(Line_Points):
                    if self.board[y][x] == 0:
                        return score, x, y
            # 棋盘已满，认定为输
            return score, -1, -1
        else:
            x, y = self.bestmove
            self.temp_point = Point(x, y)
            return score, x, y

    def findBestChess(self, turn, AI_model):
        time1 = time.time()
        self.alpha = 0
        self.belta = 0
        score, x, y = self.search(turn, AI_SEARCH_DEPTH, AI_model)
        point = Point(x, y)
        time2 = time.time()
        # print('time[%.2f] (%d, %d), score[%d] alpha[%d] belta[%d]' % (
        #     (time2 - time1), x, y, score, self.alpha, self.belta))
        self.board[y][x] = WHITE_CHESSMAN.Value
        return point, score
