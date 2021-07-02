from tools.game_pos import TansuoPos, YuhunPos

import time


class GameScene():
    def __init__(self):
        self.deep = 0

    def get_scene(self):
        '''
        Identify the current scene
             :return: Return the scene name:
             1- courtyard;
             2- Explore the interface;
             3- Chapter interface;
             4- Explore within;
             5- Yuhun menu;
             6- the beginning of the soul
             7- Industry fire begins
             8- The beginning of Himiho
        '''
        # Refuse to offer a reward
        self.yys.rejectbounty()

        # Identify courtyards, explorations, explore battle, and explore interiors separately
        maxVal, maxLoc = self.yys.find_multi_img(
            'img/JIA-CHENG.png', 'img/JUE-XING.png', 'img/TAN-SUO.png', 'img/YING-BING.png', 'img/BA-QI-DA-SHE.png', 'img/TIAO-ZHAN.png')

        scene_cof = max(maxVal)
        if scene_cof > 0.9:
            scene = maxVal.index(scene_cof)
            return scene + 1
        else:
            return 0

    def switch_to_scene(self, scene):
        '''
        Switch scene
             :param scene: The scene to be switched to: 1-8
             :return: Return True if the switch is successful; Exit directly if the switch fails
        '''
        scene_now = self.get_scene()
        self.log.info('Current scene: ' + str(scene_now))

        if scene_now == 0:
            self.log.info('The scene is not recognized yet, try again after 2s')
            time.sleep(2)
            scene_now = self.get_scene()
            self.log.info('Current scene: ' + str(scene_now))

        if scene_now == scene:
            return True
        if scene_now == 1:
            # In the courtyard
            if scene in [2, 3, 4, 5, 6, 7, 8]:
                # First draw the interface to the far right
                self.slide_x_scene(800)
                time.sleep(2)
                self.slide_x_scene(800)

                # click on the explorer selection to enter the exploration interface, if see JUE-XING img then stop
                self.click_until('Explore Button', 'img/JUE-XING.png',
                                 *TansuoPos.tansuo_denglong, 2)

                # Recursion
                self.switch_to_scene(scene)

        elif scene_now == 2:
            # Explore interface
            if scene == 3 or scene == 4:
                # Click on the last chapter
                self.click_until('Final chapter', 'img/TAN-SUO.png',
                                 *TansuoPos.last_chapter, 2)
                # Recursion
                self.switch_to_scene(scene)
            elif scene in [5, 6, 7, 8]:
                # Click the Soul button
                self.click_until('Soul Button', 'img/BA-QI-DA-SHE.png',
                                 *YuhunPos.yuhun_menu, 2)
                # Recursion
                self.switch_to_scene(scene)

        elif scene_now == 3:
            # Passanger explore_mode
            if scene == 4:
                # Click the Explore button
                self.click_until('Explore button', 'img/YING-BING.png',
                                 *TansuoPos.tansuo_btn, 2)
                # Recursion
                self.switch_to_scene(scene)
            elif scene in [5, 6, 7, 8]:
                self.click_until('Exit chapter', 'img/JUE-XING.png',
                                 *TansuoPos.quit_last_chapter, 2)
                self.switch_to_scene(scene)

        elif scene_now == 4:
            # Explore
            if scene in [2, 3]:
                # Click to exit exploration
                self.click_until_multi('Exit button', 'img/QUE-REN.png', 'img/TAN-SUO.png', 'img/JUE-XING.png',
                                 pos=TansuoPos.quit_btn[0], pos_end=TansuoPos.quit_btn[1], step_time=0.5)

                # Click to confirm
                self.click_until('Ok', 'img\\QUE-REN.png',
                                 *TansuoPos.confirm_btn, 2, False)
                # Recursion
                self.switch_to_scene(scene)

        elif scene_now == 5:
            # In the Soul menu
            if scene == 6:
                # Click Soul challenge
                self.click_until_knn('Soul challenge option', 'img/TIAO-ZHAN.png',
                                     *YuhunPos.yuhun_btn, 2, thread=20)
                # Recursion
                self.switch_to_scene(scene)
            elif scene == 7:
                # Click Sougenbi challenge
                self.click_until_knn('Sougenbi challenge option', 'img/TIAO-ZHAN.png',
                                     *YuhunPos.yeyuanhuo_btn, 2, thread=20)
                # Recursion
                self.switch_to_scene(scene)
            elif scene == 8:
                # Click Himiho challenge
                self.click_until_knn('Himiko challenge options', 'img/TIAO-ZHAN.png',
                                     *YuhunPos.beimihu_btn, 2, thread=20)
                # Recursion
                self.switch_to_scene(scene)
