import pygame as pg

# =========================
# pygame 初始化
# =========================
pg.init()


# =========================
# 字型
# =========================
def get_font(size):
    for f in ['microsoftjhenghei', 'simhei', 'stheitirelight']:
        if f in pg.font.get_fonts():
            return pg.font.SysFont(f, size)

    return pg.font.SysFont(None, size)


# 每一格大小
inter = 80

# 棋子文字大小
FONT_UI = get_font(inter // 2)


# =========================
# 顏色
# =========================
COLOR_BLACK = [0, 0, 0]
COLOR_WHITE = [255, 255, 255]
COLOR_RED = [255, 0, 0]
COLOR_BOARD = [199, 167, 82]


# =========================
# 視窗設定
# =========================
width = inter * 10
height = inter * 11

screen = pg.display.set_mode((width, height))

pg.display.set_caption("象棋")


# =========================
# 棋盤資料
# =========================

# 象棋棋盤：
# 10 列 x 9 行
row = 10
col = 9

# 初始化棋盤
chess_board = [
    [None] * col
    for i in range(row)
]


# =========================
# 棋子定義
# =========================

# 棋子資料格式：
#
# [role, side]
#
# role:
# 0 = 將 / 帥
# 1 = 士 / 仕
# 2 = 象 / 相
# 3 = 馬
# 4 = 車
# 5 = 砲 / 炮
# 6 = 卒 / 兵
#
# side:
# 0 = 黑
# 1 = 紅


# 根據 role 和 side 顯示不同文字
tags = {
    0: ["將", "帥"],
    1: ["士", "仕"],
    2: ["象", "相"],
    3: ["馬", "馬"],
    4: ["車", "車"],
    5: ["砲", "炮"],
    6: ["卒", "兵"]
}


# =========================
# 初始化棋子
# =========================

def init_chess():

    # 先清空整個棋盤
    for i in range(row):
        for j in range(col):
            chess_board[i][j] = None


    # -------------------------
    # 黑方
    # -------------------------

    # 第一排
    chess_board[0][0] = [4, 0]   # 車
    chess_board[0][1] = [3, 0]   # 馬
    chess_board[0][2] = [2, 0]   # 象
    chess_board[0][3] = [1, 0]   # 士
    chess_board[0][4] = [0, 0]   # 將
    chess_board[0][5] = [1, 0]   # 士
    chess_board[0][6] = [2, 0]   # 象
    chess_board[0][7] = [3, 0]   # 馬
    chess_board[0][8] = [4, 0]   # 車

    # 砲
    chess_board[2][1] = [5, 0]
    chess_board[2][7] = [5, 0]

    # 卒
    chess_board[3][0] = [6, 0]
    chess_board[3][2] = [6, 0]
    chess_board[3][4] = [6, 0]
    chess_board[3][6] = [6, 0]
    chess_board[3][8] = [6, 0]


    # -------------------------
    # 紅方
    # -------------------------

    # 第一排
    chess_board[9][0] = [4, 1]   # 車
    chess_board[9][1] = [3, 1]   # 馬
    chess_board[9][2] = [2, 1]   # 相
    chess_board[9][3] = [1, 1]   # 仕
    chess_board[9][4] = [0, 1]   # 帥
    chess_board[9][5] = [1, 1]   # 仕
    chess_board[9][6] = [2, 1]   # 相
    chess_board[9][7] = [3, 1]   # 馬
    chess_board[9][8] = [4, 1]   # 車

    # 炮
    chess_board[7][1] = [5, 1]
    chess_board[7][7] = [5, 1]

    # 兵
    chess_board[6][0] = [6, 1]
    chess_board[6][2] = [6, 1]
    chess_board[6][4] = [6, 1]
    chess_board[6][6] = [6, 1]
    chess_board[6][8] = [6, 1]


# 初始化一次
init_chess()


# =========================
# 重新繪製畫面
# =========================

def refresh():

    # 建立背景畫布
    bg = pg.Surface(screen.get_size())

    # 棋盤底色
    bg.fill(COLOR_BOARD)


    # =========================
    # 畫橫線
    # =========================

    for i in range(10):

        pg.draw.line(
            bg,
            COLOR_BLACK,
            [inter, inter * i + inter],
            [width - inter, inter * i + inter],
            2
        )


    # =========================
    # 畫直線
    # =========================

    for i in range(9):

        # 上半部
        pg.draw.line(
            bg,
            COLOR_BLACK,
            [inter * i + inter, inter],
            [inter * i + inter, 5 * inter],
            2
        )

        # 下半部
        pg.draw.line(
            bg,
            COLOR_BLACK,
            [inter * i + inter, 6 * inter],
            [inter * i + inter, 10 * inter],
            2
        )


    # =========================
    # 畫九宮格斜線
    # =========================

    # 黑方
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


    # 紅方
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


    # =========================
    # 畫棋子
    # =========================

    for i in range(row):

        for j in range(col):

            chess = chess_board[i][j]

            if chess is not None:

                role, side = chess


                # -------------------------
                # 棋子顏色
                # -------------------------

                if side == 0:

                    # 黑棋
                    bcolor = COLOR_BLACK
                    fcolor = COLOR_WHITE

                else:

                    # 紅棋
                    bcolor = COLOR_WHITE
                    fcolor = COLOR_RED


                # -------------------------
                # 棋盤位置 → pygame 座標
                # -------------------------

                cy = i * inter + inter
                cx = j * inter + inter


                # -------------------------
                # 畫棋子圓形
                # -------------------------

                pg.draw.circle(
                    bg,
                    bcolor,
                    [cx, cy],
                    inter // 2 - 4,
                    0
                )


                # 紅棋加黑色外框
                if side == 1:

                    pg.draw.circle(
                        bg,
                        COLOR_BLACK,
                        [cx, cy],
                        inter // 2 - 4,
                        2
                    )


                # -------------------------
                # 棋子上的文字
                # -------------------------

                text = tags[role][side]

                txt = FONT_UI.render(
                    text,
                    True,
                    fcolor
                )


                bg.blit(
                    txt,
                    txt.get_rect(
                        center=[cx, cy]
                    )
                )


    # =========================
    # 更新畫面
    # =========================

    screen.blit(bg, [0, 0])

    pg.display.update()

    return bg


# 第一次繪製
refresh()


# =========================
# 遊戲資料
# =========================

# 第幾回合
game_round = 0

# 被選到的棋子
chosen = None


# =========================
# 遊戲主迴圈
# =========================

running = True

while running:

    # 收取所有事件
    for event in pg.event.get():


        # -------------------------
        # 滑鼠放開
        # -------------------------

        if event.type == pg.MOUSEBUTTONUP:

            m_x, m_y = pg.mouse.get_pos()

            print("滑鼠位置:", m_x, m_y)


        # -------------------------
        # 按右上角 X
        # -------------------------

        if event.type == pg.QUIT:

            running = False


# =========================
# 關閉 pygame
# =========================

pg.quit()