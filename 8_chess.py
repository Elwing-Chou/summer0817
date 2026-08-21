import pygame as pg

# pygame初始化
pg.init()

# --- 字型 ---
def get_font(size):
    for f in ['microsoftjhenghei', 'simhei', 'stheitirelight']:
        if f in pg.font.get_fonts():
            return pg.font.SysFont(f, size)
    return pg.font.SysFont(None, size)

inter = 80
FONT_UI = get_font(inter//2)
# 定義顏色
COLOR_BLACK = [0, 0, 0]
COLOR_WHITE = [255, 255, 255]
COLOR_RED = [255, 0, 0]

#設定視窗
width, height = inter * 10, inter * 11
# 產生視窗
screen = pg.display.set_mode((width, height))
# 設定遊戲標題
pg.display.set_caption("象棋")

# 定義我的棋盤(10x9)
row, col = 10, 9
chess_board = [[None] * col for i in range(row)]
# 棋子: [名稱, 陣營]
# 名稱: 帥/仕....
# 陣營: 0: 黑  1: 紅
# 我初始化旗子
chess_board[0][4] = [0, 0]
chess_board[9][4] = [0, 1]

# tags: 把我的0 1 2 3轉換成帥/仕
tags = {
    0:["將", "帥"]
}

# 第幾回合
game_round = 0
# [i, j]
chosen = None

def isvalideat(chess, lasti, lastj, newi, newj):
    role, side = chess
    if role == 0:
        # special: 同一行有另外一個將或帥
        role2, side2 = chess_board[newi][newj]
        if role == role2 and not side == side2 and lastj == newj:
            return True
        # same
        return isvalidmove(chess, lasti, lastj, newi, newj)
    return False

def isvalidmove(chess, lasti, lastj, newi, newj):
    role, side = chess
    # 如果他是將或帥
    if role == 0:
        # 判斷是否只走一步
        if abs(newi-lasti) + abs(newj-lastj) == 1:
            # 黑方
            if side == 0:
                # 不用判斷舊的位置(判斷是否合理方格)
                if 0 <= newi <= 2 and 3 <= newj <= 5:
                    return True
                else:
                    return False
            # 紅方
            else:
                # 不用判斷舊的位置(判斷是否合理方格)
                if 7 <= newi <= 9 and 3 <= newj <= 5:
                    return True
                else:
                    return False
        # 如果你走的不只一步
        else:
            return False

    # 沒有核准的都return False
    return False


# 重新繪製整個畫布
def refresh():
    global chosen, game_round

    # 建立畫布bg
    bg = pg.Surface(screen.get_size())
    # 把畫布填滿某個顏色rgb
    bg.fill([199, 167, 82])
    # 畫棋盤的橫線(背景, 顏色, 開始座標, 結束座標, 寬度)
    for i in range(10):
        pg.draw.line(bg,
                     COLOR_BLACK,
                     [inter, inter*i+inter],
                     [width-inter, inter*i+inter],
                     2)
    # 畫棋盤的直線
    for i in range(9):
        pg.draw.line(bg,
                     COLOR_BLACK,
                     [inter*i+inter, inter],
                     [inter*i+inter, 5 * inter],
                     2)
        pg.draw.line(bg,
                     COLOR_BLACK,
                     [inter*i+inter, 6 * inter],
                     [inter*i+inter, 10 * inter],
                     2)
    # 畫上面的斜線
    pg.draw.line(bg,
                 COLOR_BLACK,
                 [4 * inter, inter],
                 [6 * inter, 3 * inter],
                 2)
    pg.draw.line(bg,
                 COLOR_BLACK,
                 [6 * inter, inter],
                 [4 * inter, 3 * inter],
                 2)
    # 畫下面的斜線
    pg.draw.line(bg,
                 COLOR_BLACK,
                 [4 * inter, 8 * inter],
                 [6 * inter, 10 * inter],
                 2)
    pg.draw.line(bg,
                 COLOR_BLACK,
                 [6 * inter, 8 * inter],
                 [4 * inter, 10 * inter],
                 2)

    # 畫其子
    for i in range(row):
        for j in range(col):
            chess = chess_board[i][j]
            if not chess == None:
                role, side = chess
                # 根據不同陣營, 設置不同的背景/字體顏色
                if side == 0:
                    bcolor = COLOR_BLACK
                    fcolor = COLOR_WHITE
                else:
                    bcolor = COLOR_WHITE
                    fcolor = COLOR_BLACK

                # 把你棋盤位置(0 1 2 3 4) 換成 UI座標 (80, 160, 240)
                cy, cx = i * inter + inter, j * inter + inter
                pg.draw.circle(bg, bcolor, [cx, cy], inter/2, 0)
                # 旗子上的字體
                txt = FONT_UI.render(tags[role][side], True, fcolor)
                # get_rect: 用中心座標轉左上座標
                # blit: 把字體貼在bg上
                bg.blit(txt, txt.get_rect(center=[cx, cy]))

    # 畫選取框
    if not chosen == None:
        ci, cj = chosen
        cy, cx = (ci + 1) * inter, (cj + 1) * inter
        pg.draw.rect(bg,
                     COLOR_RED,
                     [cx-inter/2, cy-inter/2, inter, inter],
                     1)

    screen.blit(bg, [0,0])
    # 對畫面進行更新(才會真的秀出來)
    pg.display.update()
    return bg

refresh()
# 建立一個永不結束的迴圈(遊戲才不會結束)
running = True
while running:
    # 收取你的遊戲任何事件(滑鼠點擊/鍵盤按鈕...)
    for event in pg.event.get():
        # 偵測滑鼠點擊以後放掉的動作
        if event.type == pg.MOUSEBUTTONUP:
            m_x, m_y = pg.mouse.get_pos()
            print(m_x, m_y)
            # 座標/80 -> (160, 80) -> (2, 1)  (180, 100) -> (2.25, 1.25)
            m_x_1, m_y_1 = m_x / inter, m_y / inter
            # (2.25, 1.25) -> (2, 1)
            m_x_1, m_y_1 = round(m_x_1), round(m_y_1)
            # (2, 1) -> 邏輯坐標系 [1][0]
            ci, cj  = m_y_1 - 1, m_x_1 - 1
            # 換成棋盤i, j
            # 點下去
            # 1. 之前已經選一顆了(移動or換一顆)
            chess = chess_board[ci][cj]
            if not chosen == None:
                # 新選的
                # 舊的棋子
                lasti, lastj = chosen
                last_chess = chess_board[lasti][lastj]
                # case 1.1 空白位置
                if chess == None:
                    # 移動
                    if isvalidmove(last_chess, lasti, lastj, ci, cj) == True:
                        chess_board[ci][cj] = last_chess
                        chess_board[lasti][lastj] = None
                        game_round = game_round + 1
                        chosen = None
                # case 1.2 有棋子
                else:
                    # case 1.2.1 我方: 換一顆
                    if chess[1] == last_chess[1]:
                        chosen = [ci, cj]
                    # case 1.2.2 敵方: 吃
                    else:
                        if isvalideat(last_chess, lasti, lastj, ci, cj) == True:
                            chess_board[ci][cj] = last_chess
                            chess_board[lasti][lastj] = None
                            game_round = game_round + 1
                            chosen = None
            # 2. 之前沒有選
            else:
                # 2.1 新的是空白
                if chess == None:
                    pass
                else:
                    # 2.2 新的不是空白: 選擇(依據game_round)
                    if chess[1] == game_round % 2:
                        chosen = [ci, cj]
            refresh()
        # 如果收到的事件是按x
        if event.type == pg.QUIT:
            # 迴圈就會變成while False
            running = False

pg.quit()