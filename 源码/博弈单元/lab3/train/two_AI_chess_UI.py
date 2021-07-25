"""两个人工智能黑白棋互相博弈，得到对不同评价函数的评价值"""

import random
from AI_alpha_beta import *
from Checkboard import *
from MyModel import Model

import pygame.gfxdraw
from DrawUI import *

Chessman = namedtuple('Chessman', 'Name Value Color')
Point = namedtuple('Point', 'X Y')
BLACK_CHESSMAN = Chessman('黑子', 1, (45, 45, 45))
WHITE_CHESSMAN = Chessman('白子', 2, (255, 255, 255))

offset = [(1, 0), (0, 1), (1, 1), (1, -1)]

def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))

CURRENT_BLACK_POINT = Point(-1, -1)
CURRENT_WHITE_POINT = Point(-1, -1)

def _get_next(cur_runner):
    if cur_runner == BLACK_CHESSMAN:
        return WHITE_CHESSMAN
    else:
        return BLACK_CHESSMAN

#让AI对局n次
GAME_MAX_COUNT = 3

def two_AI_chess_UI(x, y):

    x_model = Model()
    y_model = Model()

    x_model.my_set_weights(x)
    y_model.my_set_weights(y)

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('五子棋')

    font1 = pygame.font.SysFont('SimHei', 32)
    font2 = pygame.font.SysFont('SimHei', 72)
    fwidth, fheight = font2.size('黑方获胜')

    checkerboard = Checkerboard(Line_Points)
    cur_runner = BLACK_CHESSMAN
    winner = None

    black_win_count = 0
    white_win_count = 0

    computer_white = ChessAI(Line_Points, WHITE_CHESSMAN)
    computer_black = ChessAI(Line_Points, BLACK_CHESSMAN)

    step = 1

    while True:

        if step == 1:
            x = random.randint(0, Line_Points - 1)
            y = random.randint(0, Line_Points - 1)
            black_point = Point(x, y)
            computer_black.board[x][y] = WHITE_CHESSMAN.Value
            winner = checkerboard.drop(cur_runner, black_point)
            CURRENT_BLACK_POINT = black_point
            cur_runner = _get_next(cur_runner)
            # 合理地初始化黑白棋的当前点，防止出现错误
            computer_black.temp_point = black_point
            computer_white.temp_point = black_point
            step = 0

        if winner is None:
            computer_white.get_opponent_drop(CURRENT_BLACK_POINT)
            white_point, score_white = computer_white.findBestChess(WHITE_CHESSMAN.Value, y_model)  # 2

            CURRENT_WHITE_POINT = white_point
            # 判断是否赢得比赛
            winner = checkerboard.drop(cur_runner, white_point)
            if white_point == (-1, -1):
                winner = _get_next(cur_runner)
            if winner is not None:
                print("白棋赢了！")
                white_win_count += 1
            else:
                cur_runner = _get_next(cur_runner)

                computer_black.get_opponent_drop(CURRENT_WHITE_POINT)
                black_point, score_black = computer_black.findBestChess(BLACK_CHESSMAN.Value, x_model)  # 1

                # 判断是否赢得比赛
                CURRENT_BLACK_POINT = black_point
                winner = checkerboard.drop(cur_runner, black_point)
                if black_point == (-1, -1):
                    winner = _get_next(cur_runner)
                if winner is not None:
                    print("黑棋赢了！")
                    black_win_count += 1

                cur_runner = _get_next(cur_runner)
        # 有赢家，初始化下一局
        if winner is not None:
            if black_win_count + white_win_count == GAME_MAX_COUNT:
                # 1: black wins; 0: no winner; -1: white wins
                if black_win_count > white_win_count:
                    # print("黑棋赢了！")
                    return 1
                elif black_win_count == white_win_count:
                    return 0
                else:
                    # print("白棋赢了！")
                    return -1
            winner = None
            cur_runner = BLACK_CHESSMAN
            checkerboard = Checkerboard(Line_Points)
            step = 1
            computer_white = ChessAI(Line_Points, WHITE_CHESSMAN)
            computer_black = ChessAI(Line_Points, BLACK_CHESSMAN)

        # 在右侧打印出战况
        DrawUI._draw_left_info(screen, font1, cur_runner, black_win_count, white_win_count, DrawUI)

        # 判断最终的冠军
        if winner:
            print_text(screen, font2, (SCREEN_WIDTH - fwidth)//2, (SCREEN_HEIGHT - fheight)//2, winner.Name + '获胜', RED_COLOR)

        pygame.display.flip()