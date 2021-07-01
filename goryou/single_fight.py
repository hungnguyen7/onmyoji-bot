from gameLib.fighter import Fighter
from tools.game_pos import YuhunPos
import tools.utilities as ut

import logging


class GoryouFight(Fighter):
    '''Single player soul fighting'''

    def __init__(self, done=1, emyc=0):
        # initialization
        Fighter.__init__(self)

    def start(self):
        '''Single player battle loop'''
        mood1 = ut.Mood()
        mood2 = ut.Mood()
        mood3 = ut.Mood(3)
        while self.run:
            # Detect whether the settlement is successful in the previous step, and prevent abnormalities caused by the fact that the vibrator is opened for a moment and is not detected
            maxVal, maxLoc = self.yys.find_multi_img(
                'img/SHENG-LI.png', 'img/TIAO-DAN.png', 'img/JIN-BI.png', 'img/JIE-SU.png')
            if max(maxVal) > 0.9:
                self.get_reward(mood3, 1)

            # Click the "Challenge" button in the main menu of Evo, you need to use "lineup lock"!
            self.yys.wait_game_img_knn('img\\TIAO-ZHAN.png',
                                       self.max_win_time, thread=20)
            mood1.moodsleep()
            self.click_until_knn('Challenge button', 'img\\TIAO-ZHAN.png',
                                 *YuhunPos.tiaozhan_btn, appear=False, thread=20)

            # Check whether to enter the battle
            self.check_battle()

            # In battle, automatically click the blame
            self.click_monster()

            # Check whether it is finished
            state = self.check_end()
            mood2.moodsleep()

            # On the battle settlement page
            self.get_reward(mood3, state)
            logging.info("Back to the selection interface")

            # Check the number of games
            self.check_times()
