import pygame as pg

# pygame初始化
pg.init()

# --- 字型 ---
def get_font(size):
    for f in ['microsoftjhenghei', 'simhei', 'stheitirelight']:
        if f in pg.font.get_fonts():
            return pg.font.SysFont(f, size)
    return pg.font.SysFont(None, size)

inter = 40
FONT_UI = get_font(inter//2)
# 定義顏色
COLOR_BLACK = [0, 0, 0]
COLOR_WHITE = [255, 255, 255]

#設定視窗
width, height = inter * 10, inter * 11
# 產生視窗
screen = pg.display.set_mode((width, height))
# 設定遊戲標題
pg.display.set_caption("象棋")

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
    pg.draw.circle(bg, COLOR_BLACK, [2 * inter, inter], inter/2, 0)
    # 旗子上的字體
    txt = FONT_UI.render("馬", True, COLOR_WHITE)
    # get_rect: 用中心座標轉左上座標
    # blit: 把字體貼在bg上
    bg.blit(txt, txt.get_rect(center=[2 * inter, inter]))

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