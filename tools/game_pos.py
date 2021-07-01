class CommonPos():
    second_position = (1000, 100), (1111, 452)  # The location of the second clearing house click

    @staticmethod
    def InitPosWithClient__():
        for item in vars(CommonPos).items():
            if not '__' in item[0]:
                setattr(CommonPos, item[0], ((
                    item[1][0][0], item[1][0][1] + 35), (item[1][1][0], item[1][1][1] + 35)))


class TansuoPos():
    last_chapter = (934, 493), (1108, 572)  # The last chapter of the list
    quit_last_chapter = (913, 114), (948, 148)  # Exit the last chapter
    tansuo_btn = (787, 458), (890, 500)  # Explore button
    tansuo_denglong = (424, 118), (462, 158)  # Explore the lantern
    ready_btn = (1000, 460), (1069, 513)  # Ready button
    quit_btn = (32, 45), (58, 64)  # Exit copy
    confirm_btn = (636, 350), (739, 370)  # Exit confirmation button
    change_monster = (427, 419), (457, 452)  # Switch food click area
    quanbu_btn = (37, 574), (80, 604)  # "All" button
    n_tab_btn = (142, 288), (164, 312)  # n card label
    s_tab_btn = (33, 264), (82, 307)  # Material tags
    r_tab_btn = (216, 322), (259, 366)  # r card label
    n_slide = (168, 615), (784, 615)  # n card progress bar, from beginning to end
    gouliang_left = (161, 174), (322, 288)  # food position on the left
    gouliang_middle = (397, 218), (500, 349)  # Middle food position
    gouliang_right = (628, 293), (730, 430)  # food position on the right
    gouliang_leftback = (0, 273), (150, 393)  # Rear left food position
    gouliang_rightback = (433, 462), (567, 569)  # Rear right food position
    yaoqing_comfirm = (601, 361), (746, 406)  # Continue invitation button

    @staticmethod
    def InitPosWithClient__():
        for item in vars(TansuoPos).items():
            if not '__' in item[0]:
                setattr(TansuoPos, item[0], ((
                    item[1][0][0], item[1][0][1] + 35), (item[1][1][0], item[1][1][1] + 35)))


class YuhunPos():
    tiaozhan_btn = (995, 533), (1055, 595)    # Soul Challenge Button
    kaishizhandou_btn = (1048, 535), (1113, 604)   # Soul start battle button
    yuhun_menu = (148, 568), (206, 620)    # Soul Menu
    yuhun_btn = (147, 152), (327, 408)    # Soul option
    yeyuanhuo_btn = (476, 125), (708, 427)    # Industry original fire option
    beimihu_btn = (838, 141), (1048, 407)    # Himiko

    @staticmethod
    def InitPosWithClient__():
        for item in vars(YuhunPos).items():
            if not '__' in item[0]:
                setattr(YuhunPos, item[0], ((
                    item[1][0][0], item[1][0][1] + 35), (item[1][1][0], item[1][1][1] + 35)))
