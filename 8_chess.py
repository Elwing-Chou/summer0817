import pygame as pg

# pygame初始化
pg.init()

# --- 字型 ---
def get_font(size):
    for f in ['microsoftjhenghei', 'simhei', 'stheitirelight']:
        if f in pg.font.get_fonts():
            return pg.font.SysFont(f, size)
    return pg.font.SysFont(None, size)


FONT_UI = get_font(32)

#設定視窗
inter = 80
width, height = inter * 10, inter * 11
# 產生視窗
screen = pg.display.set_mode((width, height))
# 設定遊戲標題
pg.display.set_caption("象棋")

#
def refresh():
    # 建立畫布bg
    bg = pg.Surface(screen.get_size())
    # 把畫布填滿某個顏色rgb
    bg.fill([199, 167, 82])
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