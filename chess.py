import pygame as pg
import copy
import math

# =========================================================
# pygame 初始化
# =========================================================

pg.init()


# =========================================================
# 字型
# =========================================================

def get_font(size):
    for f in ['microsoftjhenghei', 'simhei', 'stheitirelight']:
        if f in pg.font.get_fonts():
            return pg.font.SysFont(f, size)

    return pg.font.SysFont(None, size)


inter = 80

FONT_UI = get_font(inter // 2)
FONT_INFO = get_font(28)


# =========================================================
# 顏色
# =========================================================

COLOR_BLACK = [0, 0, 0]
COLOR_WHITE = [255, 255, 255]
COLOR_RED = [220, 0, 0]
COLOR_BOARD = [199, 167, 82]
COLOR_GREEN = [0, 150, 0]


# =========================================================
# 視窗
# =========================================================

width = inter * 10
height = inter * 11

screen = pg.display.set_mode((width, height))

pg.display.set_caption("象棋")


# =========================================================
# 棋盤資料
# =========================================================

row = 10
col = 9

chess_board = [[None] * col for i in range(row)]


# =========================================================
# 棋子定義
# =========================================================

# 棋子：
#
# [role, side]
#
# role
# 0 = 將 / 帥
# 1 = 士 / 仕
# 2 = 象 / 相
# 3 = 馬
# 4 = 車
# 5 = 砲 / 炮
# 6 = 卒 / 兵
#
# side
# 0 = 黑
# 1 = 紅

tags = {
    0: ["將", "帥"],
    1: ["士", "仕"],
    2: ["象", "相"],
    3: ["馬", "馬"],
    4: ["車", "車"],
    5: ["砲", "炮"],
    6: ["卒", "兵"]
}


# =========================================================
# 棋子價值
# AI 評分會用
# =========================================================

PIECE_VALUE = {
    0: 100000,     # 將 / 帥
    1: 200,        # 士
    2: 200,        # 象
    3: 450,        # 馬
    4: 900,        # 車
    5: 500,        # 炮
    6: 100         # 卒 / 兵
}


# =========================================================
# 初始化棋盤
# =========================================================

def init_chess():

    global chess_board

    chess_board = [[None] * col for i in range(row)]

    # -----------------------------------------------------
    # 黑方
    # -----------------------------------------------------

    chess_board[0][0] = [4, 0]
    chess_board[0][1] = [3, 0]
    chess_board[0][2] = [2, 0]
    chess_board[0][3] = [1, 0]
    chess_board[0][4] = [0, 0]
    chess_board[0][5] = [1, 0]
    chess_board[0][6] = [2, 0]
    chess_board[0][7] = [3, 0]
    chess_board[0][8] = [4, 0]

    chess_board[2][1] = [5, 0]
    chess_board[2][7] = [5, 0]

    chess_board[3][0] = [6, 0]
    chess_board[3][2] = [6, 0]
    chess_board[3][4] = [6, 0]
    chess_board[3][6] = [6, 0]
    chess_board[3][8] = [6, 0]

    # -----------------------------------------------------
    # 紅方
    # -----------------------------------------------------

    chess_board[9][0] = [4, 1]
    chess_board[9][1] = [3, 1]
    chess_board[9][2] = [2, 1]
    chess_board[9][3] = [1, 1]
    chess_board[9][4] = [0, 1]
    chess_board[9][5] = [1, 1]
    chess_board[9][6] = [2, 1]
    chess_board[9][7] = [3, 1]
    chess_board[9][8] = [4, 1]

    chess_board[7][1] = [5, 1]
    chess_board[7][7] = [5, 1]

    chess_board[6][0] = [6, 1]
    chess_board[6][2] = [6, 1]
    chess_board[6][4] = [6, 1]
    chess_board[6][6] = [6, 1]
    chess_board[6][8] = [6, 1]


init_chess()


# =========================================================
# 基本工具
# =========================================================

def inside(i, j):
    """是否在棋盤範圍內"""
    return 0 <= i < 10 and 0 <= j < 9


def count_between(board, i1, j1, i2, j2):
    """
    計算兩個位置中間有多少棋子。
    只適用於橫線或直線。
    """

    count = 0

    if i1 == i2:

        start = min(j1, j2) + 1
        end = max(j1, j2)

        for j in range(start, end):

            if board[i1][j] is not None:
                count += 1

    elif j1 == j2:

        start = min(i1, i2) + 1
        end = max(i1, i2)

        for i in range(start, end):

            if board[i][j1] is not None:
                count += 1

    return count


# =========================================================
# 判斷單純棋子走法
#
# 注意：
# 這裡只判斷棋子本身的規則。
# 不處理「走完後自己是否被將軍」。
# =========================================================

def basic_valid_move(board, lasti, lastj, ci, cj, eating=False):

    if not inside(lasti, lastj):
        return False

    if not inside(ci, cj):
        return False

    chess = board[lasti][lastj]

    if chess is None:
        return False

    role, side = chess

    di = ci - lasti
    dj = cj - lastj

    adi = abs(di)
    adj = abs(dj)

    # =====================================================
    # 將 / 帥
    # =====================================================

    if role == 0:

        # 九宮限制
        if side == 0:

            if not (
                0 <= ci <= 2
                and
                3 <= cj <= 5
            ):
                return False

        else:

            if not (
                7 <= ci <= 9
                and
                3 <= cj <= 5
            ):
                return False

        # 一次只能上下左右一格
        return adi + adj == 1


    # =====================================================
    # 士 / 仕
    # =====================================================

    elif role == 1:

        # 必須斜走一格
        if adi != 1 or adj != 1:
            return False

        # 黑士只能在上方九宮
        if side == 0:

            return (
                0 <= ci <= 2
                and
                3 <= cj <= 5
            )

        # 紅仕只能在下方九宮
        else:

            return (
                7 <= ci <= 9
                and
                3 <= cj <= 5
            )


    # =====================================================
    # 象 / 相
    # =====================================================

    elif role == 2:

        # 一次斜走兩格
        if adi != 2 or adj != 2:
            return False

        # 象眼
        eye_i = (lasti + ci) // 2
        eye_j = (lastj + cj) // 2

        if board[eye_i][eye_j] is not None:
            return False

        # 黑象不能過河
        if side == 0:

            if ci > 4:
                return False

        # 紅相不能過河
        else:

            if ci < 5:
                return False

        return True


    # =====================================================
    # 馬
    # =====================================================

    elif role == 3:

        # 日字形
        if not (
            (adi == 2 and adj == 1)
            or
            (adi == 1 and adj == 2)
        ):
            return False

        # -------------------------------------------------
        # 蹩馬腿
        # -------------------------------------------------

        if adi == 2:

            # 先上下走
            leg_i = lasti + (1 if di > 0 else -1)
            leg_j = lastj

        else:

            # 先左右走
            leg_i = lasti
            leg_j = lastj + (1 if dj > 0 else -1)

        if board[leg_i][leg_j] is not None:
            return False

        return True


    # =====================================================
    # 車
    # =====================================================

    elif role == 4:

        # 車只能直線
        if lasti != ci and lastj != cj:
            return False

        # 中間不能有棋子
        return count_between(
            board,
            lasti,
            lastj,
            ci,
            cj
        ) == 0


    # =====================================================
    # 炮
    # =====================================================

    elif role == 5:

        # 炮也是直線
        if lasti != ci and lastj != cj:
            return False

        between = count_between(
            board,
            lasti,
            lastj,
            ci,
            cj
        )

        # -------------------------------------------------
        # 炮移動
        # 中間不能有棋子
        # -------------------------------------------------

        if not eating:
            return between == 0

        # -------------------------------------------------
        # 炮吃棋
        # 中間剛好要有一顆棋子
        # -------------------------------------------------

        else:
            return between == 1


    # =====================================================
    # 卒 / 兵
    # =====================================================

    elif role == 6:

        # -------------------------------------------------
        # 黑卒
        # 往下走
        # -------------------------------------------------

        if side == 0:

            # 還沒過河
            if lasti <= 4:

                return di == 1 and dj == 0

            # 過河後
            else:

                return (
                    (di == 1 and dj == 0)
                    or
                    (di == 0 and adj == 1)
                )


        # -------------------------------------------------
        # 紅兵
        # 往上走
        # -------------------------------------------------

        else:

            # 還沒過河
            if lasti >= 5:

                return di == -1 and dj == 0

            # 過河後
            else:

                return (
                    (di == -1 and dj == 0)
                    or
                    (di == 0 and adj == 1)
                )

    return False


# =========================================================
# 找將 / 帥
# =========================================================

def find_king(board, side):

    for i in range(10):

        for j in range(9):

            chess = board[i][j]

            if chess is not None:

                role, chess_side = chess

                if role == 0 and chess_side == side:
                    return i, j

    return None


# =========================================================
# 將帥是否照面
# =========================================================

def kings_face(board):

    black_king = find_king(board, 0)
    red_king = find_king(board, 1)

    if black_king is None or red_king is None:
        return False

    bi, bj = black_king
    ri, rj = red_king

    if bj != rj:
        return False

    # 中間如果沒有任何棋子
    return count_between(
        board,
        bi,
        bj,
        ri,
        rj
    ) == 0


# =========================================================
# 判斷是否被將軍
# =========================================================

def is_in_check(board, side):

    king_pos = find_king(board, side)

    if king_pos is None:
        return True

    ki, kj = king_pos

    # 將帥直接照面
    if kings_face(board):
        return True

    enemy = 1 - side

    for i in range(10):

        for j in range(9):

            chess = board[i][j]

            if chess is None:
                continue

            if chess[1] != enemy:
                continue

            # 判斷敵人是否能吃到我方將
            if basic_valid_move(
                board,
                i,
                j,
                ki,
                kj,
                eating=True
            ):
                return True

    return False


# =========================================================
# 模擬移動
# =========================================================

def simulate_move(board, lasti, lastj, ci, cj):

    new_board = copy.deepcopy(board)

    new_board[ci][cj] = new_board[lasti][lastj]
    new_board[lasti][lastj] = None

    return new_board


# =========================================================
# 完整合法性
# =========================================================

def valid_action(board, lasti, lastj, ci, cj):

    if not inside(lasti, lastj):
        return False

    if not inside(ci, cj):
        return False

    chess = board[lasti][lastj]

    if chess is None:
        return False

    target = board[ci][cj]

    role, side = chess

    # 不能走到自己人身上
    if target is not None:

        if target[1] == side:
            return False

        eating = True

    else:

        eating = False

    # 棋子自己的移動規則
    if not basic_valid_move(
        board,
        lasti,
        lastj,
        ci,
        cj,
        eating
    ):
        return False

    # 模擬走一步
    new_board = simulate_move(
        board,
        lasti,
        lastj,
        ci,
        cj
    )

    # 不能走完後自己被將軍
    if is_in_check(new_board, side):
        return False

    return True


# =========================================================
# 你原本要求的兩個函式
# =========================================================

def isvalidmove(lasti, lastj, ci, cj):

    # 目的地必須是空的
    if chess_board[ci][cj] is not None:
        return False

    return valid_action(
        chess_board,
        lasti,
        lastj,
        ci,
        cj
    )


def isvalideat(lasti, lastj, ci, cj):

    # 目的地必須有棋子
    if chess_board[ci][cj] is None:
        return False

    return valid_action(
        chess_board,
        lasti,
        lastj,
        ci,
        cj
    )


# =========================================================
# 取得某一方所有合法走法
#
# move =
# (起點i, 起點j, 終點i, 終點j)
# =========================================================

def get_all_moves(board, side):

    moves = []

    for i in range(10):

        for j in range(9):

            chess = board[i][j]

            if chess is None:
                continue

            if chess[1] != side:
                continue

            for ci in range(10):

                for cj in range(9):

                    if valid_action(
                        board,
                        i,
                        j,
                        ci,
                        cj
                    ):

                        moves.append(
                            (i, j, ci, cj)
                        )

    return moves


# =========================================================
# AI 評分
#
# 黑方 AI
#
# 分數越高 → 黑方越好
# 分數越低 → 紅方越好
# =========================================================

def evaluate_board(board):

    score = 0

    for i in range(10):

        for j in range(9):

            chess = board[i][j]

            if chess is None:
                continue

            role, side = chess

            value = PIECE_VALUE[role]

            # -------------------------------------------------
            # 卒 / 兵過河加分
            # -------------------------------------------------

            if role == 6:

                if side == 0 and i >= 5:
                    value += 60

                elif side == 1 and i <= 4:
                    value += 60

            # -------------------------------------------------
            # 黑方加分
            # 紅方扣分
            # -------------------------------------------------

            if side == 0:
                score += value
            else:
                score -= value

    return score


# =========================================================
# Minimax + Alpha Beta
# =========================================================

def minimax(board, depth, alpha, beta, maximizing):

    # 黑將不見了
    if find_king(board, 0) is None:
        return -9999999

    # 紅帥不見了
    if find_king(board, 1) is None:
        return 9999999

    if depth == 0:
        return evaluate_board(board)

    # =====================================================
    # AI 黑方
    # 找最大值
    # =====================================================

    if maximizing:

        moves = get_all_moves(board, 0)

        if len(moves) == 0:

            if is_in_check(board, 0):
                return -9999999

            return evaluate_board(board)

        best = -math.inf

        for move in moves:

            i, j, ci, cj = move

            new_board = simulate_move(
                board,
                i,
                j,
                ci,
                cj
            )

            score = minimax(
                new_board,
                depth - 1,
                alpha,
                beta,
                False
            )

            best = max(best, score)

            alpha = max(alpha, best)

            if beta <= alpha:
                break

        return best


    # =====================================================
    # 玩家紅方
    # 找最小值
    # =====================================================

    else:

        moves = get_all_moves(board, 1)

        if len(moves) == 0:

            if is_in_check(board, 1):
                return 9999999

            return evaluate_board(board)

        best = math.inf

        for move in moves:

            i, j, ci, cj = move

            new_board = simulate_move(
                board,
                i,
                j,
                ci,
                cj
            )

            score = minimax(
                new_board,
                depth - 1,
                alpha,
                beta,
                True
            )

            best = min(best, score)

            beta = min(beta, best)

            if beta <= alpha:
                break

        return best


# =========================================================
# AI 找最佳走法
# =========================================================

def find_best_move(board, depth=2):

    moves = get_all_moves(board, 0)

    if len(moves) == 0:
        return None

    best_move = None
    best_score = -math.inf

    for move in moves:

        i, j, ci, cj = move

        new_board = simulate_move(
            board,
            i,
            j,
            ci,
            cj
        )

        score = minimax(
            new_board,
            depth - 1,
            -math.inf,
            math.inf,
            False
        )

        if score > best_score:

            best_score = score
            best_move = move

    print(
        "AI 選擇:",
        best_move,
        "評分:",
        best_score
    )

    return best_move


# =========================================================
# 遊戲狀態
# =========================================================

game_round = 1

# 這裡故意設成 1
#
# side 0 = 黑 AI
# side 1 = 紅 玩家
#
# game_round % 2 == 1
# → 紅方先手

chosen = None

game_over = False
winner_text = ""


# =========================================================
# 判斷遊戲是否結束
# =========================================================

def check_game_over():

    global game_over
    global winner_text

    # 黑將被吃
    if find_king(chess_board, 0) is None:

        game_over = True
        winner_text = "紅方勝利！"
        return

    # 紅帥被吃
    if find_king(chess_board, 1) is None:

        game_over = True
        winner_text = "黑方勝利！"
        return

    side = game_round % 2

    moves = get_all_moves(
        chess_board,
        side
    )

    # 沒有合法走法
    if len(moves) == 0:

        if side == 0:

            game_over = True
            winner_text = "紅方勝利！"

        else:

            game_over = True
            winner_text = "黑方勝利！"


# =========================================================
# 畫棋盤
# =========================================================

def refresh():

    global chosen
    global game_round

    bg = pg.Surface(screen.get_size())

    bg.fill(COLOR_BOARD)


    # =====================================================
    # 橫線
    # =====================================================

    for i in range(10):

        pg.draw.line(
            bg,
            COLOR_BLACK,
            [inter, inter * i + inter],
            [width - inter, inter * i + inter],
            2
        )


    # =====================================================
    # 直線
    # =====================================================

    for i in range(9):

        pg.draw.line(
            bg,
            COLOR_BLACK,
            [inter * i + inter, inter],
            [inter * i + inter, 5 * inter],
            2
        )

        pg.draw.line(
            bg,
            COLOR_BLACK,
            [inter * i + inter, 6 * inter],
            [inter * i + inter, 10 * inter],
            2
        )


    # =====================================================
    # 九宮
    # =====================================================

    pg.draw.line(
        bg,
        COLOR_BLACK,
        [4 * inter, inter],
        [6 * inter, 3 * inter],
        2
    )

    pg.draw.line(
        bg,
        COLOR_BLACK,
        [6 * inter, inter],
        [4 * inter, 3 * inter],
        2
    )

    pg.draw.line(
        bg,
        COLOR_BLACK,
        [4 * inter, 8 * inter],
        [6 * inter, 10 * inter],
        2
    )

    pg.draw.line(
        bg,
        COLOR_BLACK,
        [6 * inter, 8 * inter],
        [4 * inter, 10 * inter],
        2
    )


    # =====================================================
    # 楚河漢界
    # =====================================================

    river_text = FONT_INFO.render(
        "楚 河                 漢 界",
        True,
        COLOR_BLACK
    )

    bg.blit(
        river_text,
        river_text.get_rect(
            center=[
                width // 2,
                int(5.5 * inter)
            ]
        )
    )


    # =====================================================
    # 棋子
    # =====================================================

    for i in range(row):

        for j in range(col):

            chess = chess_board[i][j]

            if chess is None:
                continue

            role, side = chess

            if side == 0:

                bcolor = COLOR_BLACK
                fcolor = COLOR_WHITE

            else:

                bcolor = COLOR_WHITE
                fcolor = COLOR_RED


            cy = i * inter + inter
            cx = j * inter + inter


            # 棋子
            pg.draw.circle(
                bg,
                bcolor,
                [cx, cy],
                inter // 2 - 4,
                0
            )


            # 外框
            pg.draw.circle(
                bg,
                COLOR_BLACK,
                [cx, cy],
                inter // 2 - 4,
                2
            )


            txt = FONT_UI.render(
                tags[role][side],
                True,
                fcolor
            )


            bg.blit(
                txt,
                txt.get_rect(
                    center=[cx, cy]
                )
            )


    # =====================================================
    # 選取框
    # =====================================================

    if chosen is not None:

        ci, cj = chosen

        cy = (ci + 1) * inter
        cx = (cj + 1) * inter

        pg.draw.rect(
            bg,
            COLOR_RED,
            [
                cx - inter / 2,
                cy - inter / 2,
                inter,
                inter
            ],
            3
        )


    # =====================================================
    # 顯示目前回合
    # =====================================================

    if game_over:

        msg = winner_text

    else:

        if game_round % 2 == 0:

            msg = "黑方 AI 思考中..."

        else:

            msg = "紅方玩家回合"


    txt = FONT_INFO.render(
        msg,
        True,
        COLOR_BLACK
    )

    bg.blit(
        txt,
        [20, 10]
    )


    # =====================================================
    # 將軍提示
    # =====================================================

    if not game_over:

        side = game_round % 2

        if is_in_check(
            chess_board,
            side
        ):

            check_txt = FONT_INFO.render(
                "將軍！",
                True,
                COLOR_RED
            )

            bg.blit(
                check_txt,
                [width - 120, 10]
            )


    screen.blit(bg, [0, 0])

    pg.display.update()


# =========================================================
# AI 走棋
# =========================================================

def ai_turn():

    global game_round
    global chosen

    # AI 黑方
    move = find_best_move(
        chess_board,
        depth=2
    )

    if move is None:

        check_game_over()
        return

    lasti, lastj, ci, cj = move

    chess_board[ci][cj] = chess_board[lasti][lastj]
    chess_board[lasti][lastj] = None

    game_round += 1

    chosen = None

    check_game_over()

    refresh()


# =========================================================
# 第一次畫面
# =========================================================

refresh()


# =========================================================
# 主程式
# =========================================================

running = True

clock = pg.time.Clock()


while running:

    # =====================================================
    # AI 回合
    # =====================================================

    if (
        not game_over
        and
        game_round % 2 == 0
    ):

        refresh()

        # 讓畫面先顯示 AI 思考中
        pg.time.delay(200)

        ai_turn()


    # =====================================================
    # 事件
    # =====================================================

    for event in pg.event.get():

        # -------------------------------------------------
        # 關閉遊戲
        # -------------------------------------------------

        if event.type == pg.QUIT:

            running = False


        # -------------------------------------------------
        # 滑鼠點擊
        # -------------------------------------------------

        if event.type == pg.MOUSEBUTTONUP:

            # 遊戲結束不能再下
            if game_over:
                continue

            # AI 回合不能操作
            if game_round % 2 == 0:
                continue


            m_x, m_y = pg.mouse.get_pos()


            # ---------------------------------------------
            # 轉換成棋盤座標
            # ---------------------------------------------

            m_x_1 = round(
                m_x / inter
            )

            m_y_1 = round(
                m_y / inter
            )

            ci = m_y_1 - 1
            cj = m_x_1 - 1


            # ---------------------------------------------
            # 防止點到棋盤外造成 IndexError
            # ---------------------------------------------

            if not inside(ci, cj):

                chosen = None
                refresh()
                continue


            chess = chess_board[ci][cj]


            # =================================================
            # 已經選了一顆棋
            # =================================================

            if chosen is not None:

                lasti, lastj = chosen

                last_chess = chess_board[lasti][lastj]


                # ---------------------------------------------
                # 點空白
                # ---------------------------------------------

                if chess is None:

                    if isvalidmove(
                        lasti,
                        lastj,
                        ci,
                        cj
                    ):

                        chess_board[ci][cj] = last_chess
                        chess_board[lasti][lastj] = None

                        game_round += 1

                        chosen = None

                        check_game_over()


                # ---------------------------------------------
                # 點到棋子
                # ---------------------------------------------

                else:

                    # 同隊
                    if chess[1] == last_chess[1]:

                        chosen = [ci, cj]


                    # 敵人
                    else:

                        if isvalideat(
                            lasti,
                            lastj,
                            ci,
                            cj
                        ):

                            chess_board[ci][cj] = last_chess
                            chess_board[lasti][lastj] = None

                            game_round += 1

                            chosen = None

                            check_game_over()


            # =================================================
            # 還沒有選棋
            # =================================================

            else:

                if chess is not None:

                    # 只能選自己的棋
                    if chess[1] == game_round % 2:

                        chosen = [ci, cj]


            refresh()


    clock.tick(60)


# =========================================================
# 關閉 pygame
# =========================================================

pg.quit()