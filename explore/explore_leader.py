from explore.explore import ExploreFight
from tools.game_pos import TansuoPos
import tools.utilities as ut
from tools.logsystem import MyLog

import random
import time


class ExploreLeader(ExploreFight):
    '''Team Exploration Captain
    
    '''

    def __init__(self, hwnd=0, delay=False):
        '''
        initialization
             :param hwnd=0: Specified window handle: 0-No; other-window handle
             :param mode=0: food mode: 0-normal mode, 1-row food after team
             :param delay=False: After completing a round of exploration, whether to wait for 1 second before inviting the next round
        '''
        ExploreFight.__init__(self, hwnd=hwnd, mode=1)
        self.delay = delay
        self.log = MyLog.dlogger

    def prev_scene(self):
        '''
        Swipe to the previous page
        '''
        x0 = random.randint(510, 1126)
        x1 = x0 - 500
        y0 = random.randint(110, 210)
        y1 = random.randint(110, 210)
        self.yys.mouse_drag_bg((x1, y1), (x0, y0))

    def start(self):
        '''
        start fighting
        '''
        mood1 = ut.Mood(3)
        mood2 = ut.Mood(3)
        mood3 = ut.Mood()
        scene = self.get_scene()
        if scene == 4:
            self.log.info('Explored and ready')
        else:
            self.log.warning('Please check if you have entered the exploration and exit')
            return

        while self.run:
            # Detect the current scene
            maxVal_list, maxLoc_list = self.yys.find_multi_img(
                'img/DUI.png', 'img/YING-BING.png')
            if maxVal_list[0] < 0.8 and maxVal_list[1] > 0.8:
                # The captain quits and ends
                self.log.warning('The team member has exited, the script ends')
                self.yys.quit_game()

            # Start fighting monsters
            i = 0
            ok = False
            while self.run:
                if i >= 4:
                    break
                result = self.fight_moster(mood1, mood2)
                if result == 1:
                    ok = True
                    continue
                elif result == 2:
                    break
                else:
                    self.log.info('Move to the next scene')
                    self.next_scene()
                    i += 1

            if not ok:
                # No experience to blame, just hit one
                fight_pos = self.yys.find_game_img('img/FIGHT.png')
                while not fight_pos:
                    self.prev_scene()
                    fight_pos = self.yys.find_game_img('img/FIGHT.png')
                # Attack monster
                self.yys.mouse_click_bg(fight_pos)
                self.log.info('Has entered the battle')

                # Waiting for shikigami to prepare
                self.yys.wait_game_img_knn('img/ZHUN-BEI.png', thread=30)
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

            # Exit exploration
            self.log.info('End this round of exploration')
            # Click to exit exploration
            self.click_until_multi('Exit button', 'img/QUE-REN.png', 'img/TAN-SUO.png', 'img/JUE-XING.png',
                                   pos=TansuoPos.quit_btn[0], pos_end=TansuoPos.quit_btn[1], step_time=0.5)

            # Click to confirm
            self.click_until('Confirm button', 'img/QUE-REN.png',
                             *TansuoPos.confirm_btn, 2, False)

            # Wait for the driver to exit for 1s
            if self.delay:
                time.sleep(1)

            # Next round of automatic invitation
            self.yys.wait_game_img('img/QUE-DING.png', self.max_win_time)
            time.sleep(0.5)
            self.click_until('Continue to invite', 'img/QUE-DING.png', *
                             TansuoPos.yaoqing_comfirm, mood3.get1mood()/1000, False)

            # Check the number of games
            self.check_times()
