from explore.explore import ExploreFight
from tools.game_pos import TansuoPos
from tools.logsystem import MyLog
import tools.utilities as ut

import time


class ExplorePassenger(ExploreFight):
    '''
    Explore team members
    '''

    def __init__(self, hwnd=0):
        '''
        initialization
        '''
        ExploreFight.__init__(self, hwnd=hwnd)
        self.log = MyLog.plogger
        self.start_time = time.time()

    def start(self):
        '''
        start fighting
        '''
        mood = ut.Mood(3)
        mood1 = ut.Mood(3)
        scene = self.get_scene()
        if scene == 4:
            self.log.info('Explored and ready')
        else:
            self.log.warning('Please check if you have entered the exploration and exit')
            return

        while self.run:
            # Detect the current scene
            maxVal_list, _ = self.yys.find_multi_img(
                'img/DUI.png', 'img/YING-BING.png')
            # print(maxVal_list)
            if maxVal_list[0] < 0.8 and maxVal_list[1] > 0.8:
                self.start_time = time.time()

                # The captain quits, then quits
                self.log.info('The captain has exited, follow to exit')
                self.switch_to_scene(3)

                # Waiting for invitation
                js_loc = self.yys.wait_game_img(
                    'img/JIE-SHOU.png', self.max_win_time)
                if js_loc:
                    # Click to accept the invitation
                    if self.yys.find_game_img('img/JIE-SHOU.png'):
                        self.click_until('accept an invitation', 'img/JIE-SHOU.png', (127, js_loc[1]+34), appear=False)
                        self.log.info('accept an invitation')

                # Check the number of games
                self.check_times()

            elif maxVal_list[0] > 0.8 and maxVal_list[1] < 0.8:
                self.start_time = time.time()

                # Entering the battle, waiting for the shikigami to prepare
                self.yys.wait_game_img_knn('img/ZHUN-BEI.png', thread=30)
                self.log.info('Shikigami is ready')

                # Check food experience
                self.check_exp_full()

                # Click prepare until you enter the battle
                self.click_until_knn('Ready button', 'img/ZHUN-BEI.png', *
                            TansuoPos.ready_btn, mood1.get1mood()/1000, False, thread=30)

                # Check whether it is finished
                state = self.check_end()
                mood.moodsleep()

                # Click to check out
                self.get_reward(mood, state)

            else:
                # Others, do nothing
                time.sleep(0.5)
                if time.time() - self.start_time > self.max_win_time:
                    self.yys.quit_game()
