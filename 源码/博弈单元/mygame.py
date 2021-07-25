"""人工智能五子棋"""
from AI_alpha_beta import *
from Checkboard import *
from DrawUI import *
#from MyModel import *
from capture import *
from move import *

Chessman = namedtuple('Chessman', 'Name Value Color')
Point = namedtuple('Point', 'X Y')
BLACK_CHESSMAN = Chessman('黑子', 1, (45, 45, 45))
WHITE_CHESSMAN = Chessman('白子', 2, (255, 255, 255))

offset = [(1, 0), (0, 1), (1, 1), (1, -1)]

def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))


def main():

    checkerboard = Checkerboard(Line_Points)
    cur_runner = BLACK_CHESSMAN
    winner = None
    computer = ChessAI(Line_Points, WHITE_CHESSMAN)

    # 加载网络模型
    #AI_model = Model()
    black_win_count = 0
    white_win_count = 0
    init_position()

    while True:
        # 控制下棋进程
        
        a = list(capture())
        click_point = Point(a[0], a[1])

        winner = checkerboard.drop(cur_runner, click_point)
        if winner is None:
            cur_runner = _get_next(cur_runner)
            computer.get_opponent_drop(click_point)
            # AI生成白棋,findBestChess返回坐标
            AI_point, score = computer.findBestChess(WHITE_CHESSMAN.Value)  # 2
        
            put_chess(-2*AI_point.X+10+1.25,2.5*AI_point.Y+10) #math
            #put_chess2(AI_point.X,AI_point.Y) #deeplearning 
            init_position()
            #f = open("drop_point.txt", "w")
            #f.write(str(AI_point.X) + " " + str(AI_point.Y))
            #f.close()

            # 判断是否赢得比赛
            winner = checkerboard.drop(cur_runner, AI_point)
            if winner is not None:
                exit(0)
            cur_runner = _get_next(cur_runner)
        else:
            exit(0)


def _get_next(cur_runner):
    if cur_runner == BLACK_CHESSMAN:
        return WHITE_CHESSMAN
    else:
        return BLACK_CHESSMAN

if __name__ == '__main__':
    main()