from gameLib.fighter import Fighter
from tools.game_pos import CommonPos, YuhunPos
from tools.logsystem import MyLog
import tools.utilities as ut

import time


class DriverFighter(Fighter):
    '''Soul combat driver program, parameter mode'''

    def __init__(self, emyc=0, hwnd=0):
        # initialization
        Fighter.__init__(self, emyc, hwnd)
        self.log = MyLog.dlogger

    def start(self):
        '''Single Man Soul Driver'''
        # Set click fatigue
        mood1 = ut.Mood()
        mood2 = ut.Mood()
        mood3 = ut.Mood(3)

        # Main loop of battle
        self.yys.wait_game_img('img\\KAI-SHI-ZHAN-DOU.png',
                               self.max_win_time)
        while self.run:
            # The driver clicks to start the battle and needs to lock the Soul lineup
            mood1.moodsleep()
            self.log.info('Driver: Click the start battle button')
            self.click_until('Start battle button', 'img\\KAI-SHI-ZHAN-DOU.png', *
                             YuhunPos.kaishizhandou_btn, mood2.get1mood()/1000, False)
            
            # Check whether to enter the battle
            self.check_battle()

            # In battle, mark yourself as God
            self.mitama_team_click()

            # Has entered the battle, the driver automatically clicks the blame
            self.click_monster()

            # Check whether it is finished
            state = self.check_end()
            mood2.moodsleep()

            # On the battle settlement page
            self.get_reward(mood3, state)

            # Waiting for the next round
            self.log.info('Driver: Waiting for the next round')
            start_time = time.time()
            while time.time() - start_time <= 20 and self.run:
                if(self.yys.wait_game_img('img\\KAI-SHI-ZHAN-DOU.png', 1, False)):
                    self.log.info('Driver: Enter the team')
                    break

                # Click the default invitation
                if self.yys.find_game_img('img\\ZI-DONG-YAO-QING.png'):
                    self.yys.mouse_click_bg((497, 319))
                    time.sleep(0.2)
                    self.yys.mouse_click_bg((674, 384))
                    self.log.info('Driver: Automatic invitation')

            # Check the number of games
            self.check_times()
