from gameLib.fighter import Fighter
from tools.game_pos import YuhunPos
import tools.utilities as ut

import configparser


class SingleFight(Fighter):
    '''Single player soul fighting, default parameters'''

    def __init__(self, done=1, emyc=0):
        # initialization
        Fighter.__init__(self, emyc)

        # Read configuration file
        conf = configparser.ConfigParser()
        conf.read('conf.ini')
        self.run_submode = conf.getint('mitama', 'run_submode')

    def start(self):
        '''Single player battle loop'''
        mood1 = ut.Mood()
        mood2 = ut.Mood()
        mood3 = ut.Mood(3)
        if self.run_submode == 0:
            self.switch_to_scene(6)
        elif self.run_submode == 1:
            self.switch_to_scene(7)
        elif self.run_submode == 2:
            self.switch_to_scene(8)
        while self.run:
            # Click on the "Challenge" button in the main menu of Soul, you need to use "lineup lock'！
            self.yys.wait_game_img_knn(
                'img\\TIAO-ZHAN.png', max_time=self.max_win_time, thread=20)
            mood1.moodsleep()
            self.yys.mouse_click_bg(*YuhunPos.tiaozhan_btn)
            self.click_until_knn('Challenge button', 'img\\TIAO-ZHAN.png',
                                 *YuhunPos.tiaozhan_btn, appear=False, thread=20)

            # Check whether to enter the battle
            self.check_battle()

            # In battle, mark yourself as God
            self.mitama_team_click()

            # In battle, automatically click the blame
            self.click_monster()

            # Check whether it is finished
            state = self.check_end()
            mood2.moodsleep()

            # On the battle settlement page
            self.get_reward(mood3, state)
            self.log.info("Back to the selection interface")

            # Check the number of games
            self.check_times()
