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

# 重新繪製整個畫布
def refresh():
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
    pg.draw.rect(bg,
                 COLOR_RED,
                 [2*inter-inter/2, inter-inter/2, inter, inter],
                 1)

    screen.blit(bg, [0,0])
    # 對畫面進行更新(才會真的秀出來)
    pg.display.update()
    return bg

refresh()
# 建立一個永不結束的迴圈(遊戲才不會結束)
# 第幾回合
game_round = 0
chosen = None
running = True
while running:
    # 收取你的遊戲任何事件(滑鼠點擊/鍵盤按鈕...)
    for event in pg.event.get():
        # 偵測滑鼠點擊以後放掉的動作
        if event.type == pg.MOUSEBUTTONUP:
            m_x, m_y = pg.mouse.get_pos()
        # 如果收到的事件是按x
        if event.type == pg.QUIT:
            # 迴圈就會變成while False
            running = False

pg.quit()