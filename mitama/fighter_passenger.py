from gameLib.fighter import Fighter
from tools.game_pos import TansuoPos
from tools.logsystem import MyLog
import tools.utilities as ut

import time


class FighterPassenger(Fighter):
    '''Passenger program of Soul battle, parameter mode'''

    def __init__(self, emyc=0, hwnd=0, mark=True):
        '''
        initialization
             :param emyc=0: point monster setting: 0-no point blame
             :param hwnd=0: Specified window handle: 0-No; other-window handle
             :param mark=True: Whether to enable the mark function globally
        '''
        Fighter.__init__(self, emyc, hwnd)
        self.log = MyLog.plogger
        self.mark = mark

    def start(self):
        '''Single passenger'''
        # Set click fatigue
        mood2 = ut.Mood()
        mood3 = ut.Mood(3)

        # Main loop of battle
        while self.run:
            # Check whether to enter the battle
            self.check_battle()

            # In battle, mark yourself as God
            if self.mark:
                self.mitama_team_click()

            # Has entered the battle, the passengers automatically click the blame
            self.click_monster()

            # Check whether it is finished
            state = self.check_end()
            mood2.moodsleep()

            # On the battle settlement page
            self.get_reward(mood3, state)

            # Waiting for the next round
            self.log.info('Passenger: Waiting for the next round')
            start_time = time.time()
            while time.time() - start_time <= 5 and self.run:
                # Check if you are back in the team
                if(self.yys.wait_game_img('img\\XIE-ZHAN-DUI-WU.png', 1, False)):
                    self.log.info('Passenger: Enter the team')
                    break

                # Check whether there is an invitation to the soul
                yuhun_loc = self.yys.wait_game_img(
                    'img\\YU-HUN.png', 1, False)
                if yuhun_loc:
                    # Click to automatically accept the invitation
                    if self.yys.find_game_img('img\\ZI-DONG-JIE-SHOU.png'):
                        self.yys.mouse_click_bg((210, yuhun_loc[1]))
                        self.log.info('Passenger: Automatically accept invitation')

                    # Click Normal to accept the invitation
                    elif self.yys.find_game_img('img\\JIE-SHOU.png'):
                        self.yys.mouse_click_bg((125, yuhun_loc[1]))
                        self.log.info('Passenger: accept an invitation')
            
            # Check the number of games
            self.check_times()
