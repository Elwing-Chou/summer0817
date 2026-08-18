# 遊戲腳本位於此檔案。

# 宣告該遊戲使用的角色。 color 參數
# 為角色的名稱著色。

define master = Character("[master_name]")
define cat = Character("奇怪的貓")

# 遊戲從這裡開始。

label start:

    # 顯示背景。 預設情況下，它使用佔位符，但您可以
    # 將檔案（名為 "bg room.png" 或 "bg room.jpg"）新增至
    # images 目錄來顯示它。

    scene bg forest:
        xysize (1920, 1080)

    # 這顯示了一個角色精靈。 使用了佔位符，但您可以
    # 透過將名為 "eileen happy.png" 的檔案
    # 新增至 images 目錄來取代它。

    show master normal:
        align (0.1, 0.5)
        fit "contain"
        ysize 800

    show cat normal:
        align (0.9, 0.5)
        fit "contain"
        ysize 600

    # 這些顯示對話行。
    cat "要跟我玩個遊戲才能通過"
    cat "你叫什麼名字"

    $ master_name = renpy.input("請輸入姓名")

    cat "喔 你叫 [master_name]"

# 控制第幾場
$ total = 5
$ p1win, p2win = 0, 0
$ i = 0
label game:
    cat "[i]/[total]"
    menu:
        "剪刀":
            $ p1 = 0
        "石頭":
            $ p1 = 1
        "布":
            $ p1 = 2
    $ p2 = renpy.random.randint(0, 2)
    # 主人公show
    if p1 == 0:
        show master scissor:
            align (0.1, 0.5)
            fit "contain"
            ysize 800
    elif p1 == 1:
        show master stone:
            align (0.1, 0.5)
            fit "contain"
            ysize 800
    else:
        show master paper:
            align (0.1, 0.5)
            fit "contain"
            ysize 800
    # 貓show
    if p2 == 0:
        show cat scissor:
            align (0.9, 0.5)
            fit "contain"
            ysize 800
    elif p2 == 1:
        show cat stone:
            align (0.9, 0.5)
            fit "contain"
            ysize 800
    else:
        show cat paper:
            align (0.9, 0.5)
            fit "contain"
            ysize 800

    # 之前剪刀石頭布
    if p1 == (p2 + 1) % 3:
        $ p1win = p1win + 1
        master "我贏了"
    elif p2 == (p1 + 1) % 3:
        $ p2win = p2win + 1
        master "我輸了"
    else:
        master "平手"

    $ i = i + 1
    if i < 5:
        jump game
    else:
        jump final


label final:
    if p1win > p2win:
        "我贏了"
    elif p2win > p1win:
        "貓贏了"
    else:
        "平手"







