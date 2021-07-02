from gameLib.fighter import Fighter
from tools.game_pos import TansuoPos
import tools.utilities as ut

import configparser
import logging
import random
import time


class ExploreFight(Fighter):
    def __init__(self, hwnd=0, mode=0):
        '''
        initialization
             :param hwnd=0: Specified window handle: 0-No; other-window handle
             :param mode=0: Food mode: 0-normal mode, 1-row dog food after team
        '''
        Fighter.__init__(self, hwnd=hwnd)

        # Read configuration file
        conf = configparser.ConfigParser()
        conf.read('conf.ini')

        # Read food configuration
        if mode == 0:
            raw_gouliang = conf.get('explore', 'gouliang')
        else:
            raw_gouliang = conf.get('explore', 'gouliang_b')
        if len(raw_gouliang) == 2:
            self.gouliang = None
        elif len(raw_gouliang) == 3:
            self.gouliang = [int(raw_gouliang[1])]
        elif len(raw_gouliang) == 6:
            self.gouliang = [int(raw_gouliang[1]), int(raw_gouliang[4])]
        elif len(raw_gouliang) == 9:
            self.gouliang = [int(raw_gouliang[1]), int(
                raw_gouliang[4]), int(raw_gouliang[7])]

        # Read other configuration
        self.fight_boss_enable = conf.getboolean(
            'explore', 'fight_boss_enable')
        self.slide_shikigami = conf.getboolean('explore', 'slide_shikigami')
        self.slide_shikigami_progress = conf.getint(
            'explore', 'slide_shikigami_progress')
        self.change_shikigami = conf.getint('explore', 'change_shikigami')

    def next_scene(self):
        '''
        Move to the next scene, 400 pixels at a time
        '''
        x0 = random.randint(510, 1126)
        x1 = x0 - 500
        y0 = random.randint(110, 210)
        y1 = random.randint(110, 210)
        self.yys.mouse_drag_bg((x0, y0), (x1, y1))

    def check_exp_full(self):
        '''
        Check food experience and automatically change food
        Food sequence, 1-left; 2-middle; 3-right; 4-left rear; 5-right rear
        '''
        if self.gouliang == None:
            return

        # food experience judgment
        gouliang = []
        if 1 in self.gouliang:
            gouliang.append(self.yys.find_game_img(
                'img\\MAN2.png', 1, *TansuoPos.gouliang_left, 1, 0.8))
        if 2 in self.gouliang:
            gouliang.append(self.yys.find_game_img(
                'img\\MAN2.png', 1, *TansuoPos.gouliang_middle, 1, 0.8))
        if 3 in self.gouliang:
            gouliang.append(self.yys.find_game_img(
                'img\\MAN2.png', 1, *TansuoPos.gouliang_right, 1, 0.8))
        if 4 in self.gouliang:
            gouliang.append(self.yys.find_game_img(
                'img\\MAN2.png', 1, *TansuoPos.gouliang_leftback, 1, 0.8))
        if 5 in self.gouliang:
            gouliang.append(self.yys.find_game_img(
                'img\\MAN2.png', 1, *TansuoPos.gouliang_rightback, 1, 0.8))

        # Exit if not full
        res = False
        for item in gouliang:
            res = res or bool(item)
        if not res:
            return

        # Start changing food
        while self.run:
            # Click on the position of food
            self.yys.mouse_click_bg(*TansuoPos.change_monster)
            if self.yys.wait_game_img('img\\QUAN-BU.png', 3, False):
                break
        time.sleep(1)

        # Click the "All" option
        self.yys.mouse_click_bg(*TansuoPos.quanbu_btn)
        time.sleep(1)

        # Click on the card
        if self.change_shikigami == 1:
            self.yys.mouse_click_bg(*TansuoPos.n_tab_btn)
        elif self.change_shikigami == 0:
            self.yys.mouse_click_bg(*TansuoPos.s_tab_btn)
        elif self.change_shikigami == 2:
            self.yys.mouse_click_bg(*TansuoPos.r_tab_btn)
        time.sleep(1)

        # Drag and drop progress bar
        if self.slide_shikigami:
            # Read coordinate range
            star_x = TansuoPos.n_slide[0][0]
            end_x = TansuoPos.n_slide[1][0]
            length = end_x - star_x

            # Calculate the drag and drop range
            pos_end_x = int(star_x + length/100*self.slide_shikigami_progress)
            pos_end_y = TansuoPos.n_slide[0][1]

            self.yys.mouse_drag_bg(
                TansuoPos.n_slide[0], (pos_end_x, pos_end_y))
            time.sleep(1)

        # Change dog food
        for i in range(0, len(self.gouliang)):
            if gouliang[i]:
                if self.gouliang[i] == 1:
                    self.yys.mouse_drag_bg((422, 520), (955, 315))
                elif self.gouliang[i] == 2:
                    self.yys.mouse_drag_bg((309, 520), (554, 315))
                elif self.gouliang[i] == 3:
                    self.yys.mouse_drag_bg((191, 520), (167, 315))
                elif self.gouliang[i] == 4:
                    self.yys.mouse_drag_bg((309, 520), (829, 315))
                elif self.gouliang[i] == 5:
                    self.yys.mouse_drag_bg((191, 520), (301, 315))
                ut.mysleep(1000)

    def find_exp_moster(self):
        '''
        Looking for experience monsters
             return: Return to the position of the attack icon of the experience monster successfully; return -1 on failure
        '''
        # Find experience icon
        exp_pos = self.yys.find_color(
            ((2, 205), (1127, 545)), (140, 122, 44), 2)
        if exp_pos == -1:
            exp_pos = self.yys.find_img_knn(
                'img\\EXP.png', 1, (2, 205), (1127, 545))
            if exp_pos == (0, 0):
                return -1
            else:
                exp_pos = (exp_pos[0]+2, exp_pos[1]+205)

        # Find the location of the experience monster attack icon
        find_pos = self.yys.find_game_img(
            'img\\FIGHT.png', 1, (exp_pos[0]-150, exp_pos[1]-250), (exp_pos[0]+150, exp_pos[1]-50))
        if not find_pos:
            return -1

        # Return to the position of the experience monster attack icon
        fight_pos = ((find_pos[0]+exp_pos[0]-150),
                     (find_pos[1]+exp_pos[1]-250))
        return fight_pos

    def find_boss(self):
        '''
        Find the boss
             :return: Return the position of the attack icon of the BOSS successfully; return -1 on failure
        '''
        # Find the location of the boss attack icon
        find_pos = self.yys.find_game_img(
            'img\\BOSS.png', 1, (2, 205), (1127, 545))
        if not find_pos:
            return -1

        # Return to the position of the boss attack icon
        fight_pos = ((find_pos[0]+2), (find_pos[1]+205))
        return fight_pos

    def fight_moster(self, mood1, mood2):
        '''
        Fighting experience monsters
             :return: Return 1 after playing ordinary monsters; return 2 after playing bosses; return -1 if experience monsters are not found; return -2 if experience monsters and bosses are not found
        '''
        while self.run:
            mood1.moodsleep()
            # Check whether to enter the exploration interface
            self.yys.wait_game_img('img\\YING-BING.png')
            self.log.info('Enter the map')

            # Look for the experience monster, look for the boss if you don’t find it, and exit if you don’t find it
            fight_pos = self.find_exp_moster()
            boss = False
            if fight_pos == -1:
                if self.fight_boss_enable:
                    fight_pos = self.find_boss()
                    boss = True
                    if fight_pos == -1:
                        self.log.info('No experience monsters and bosses found')
                        return -2
                else:
                    self.log.info('No experience monster found')
                    return -1

            # Attack monster
            # click_until(tag, *, pos, _)
            self.click_until('Attack', 'img/YING-BING.png', fight_pos, step_time=0.3, appear=False)
            self.log.info('Has entered the battle')

            # Waiting for shikigami to prepare
            self.yys.wait_game_img_knn('img\\ZHUN-BEI.png', thread=30)
            self.log.info('Shikigami is ready')

            # Check food experience
            self.check_exp_full()

            # Click prepare until you enter the battle
            self.click_until_knn('Ready button', 'img/ZHUN-BEI.png', *
                            TansuoPos.ready_btn, mood1.get1mood()/1000, False, 30)

            # Check if it's done
            state = self.check_end()
            mood1.moodsleep()

            # On the battle settlement page
            self.get_reward(mood2, state)

            # Return result
            if boss:
                return 2
            else:
                return 1

    def start(self):
        '''Single player to explore the main loop'''
        mood1 = ut.Mood(3)
        mood2 = ut.Mood(3)
        while self.run:
            # Enter exploration
            self.switch_to_scene(4)

            # Start fighting monsters
            i = 0
            while self.run:
                if i >= 4:
                    break
                result = self.fight_moster(mood1, mood2)
                if result == 1:
                    continue
                elif result == 2:
                    break
                else:
                    self.log.info('Move to the next scene')
                    self.next_scene()
                    i += 1

            # Exit exploration
            self.switch_to_scene(3)
            self.log.info('End this round of exploration')
            time.sleep(0.5)

            # Check the number of games
            self.check_times()
