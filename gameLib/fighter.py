from gameLib.game_ctl import GameControl
from gameLib.game_scene import GameScene
from tools.logsystem import MyLog
from tools.game_pos import TansuoPos, YuhunPos
import tools.utilities as ut

import configparser
import os
import random
import threading
import time
import win32gui


class Fighter(GameScene):

    def __init__(self, emyc=0, hwnd=0):
        '''
        initialization
             : param emyc=0: point monster setting: 0-no point monster
             : param hwnd=0: Specified window handle: 0-No; other-window handle
        '''
        # Initial parameters
        self.emyc = emyc
        self.run = True

        # Read configuration file
        conf = configparser.ConfigParser()
        conf.read('conf.ini')
        self.client = conf.getint('DEFAULT', 'client')
        quit_game_enable = conf.getboolean('watchdog', 'watchdog_enable')
        self.max_op_time = conf.getint('watchdog', 'max_op_time')
        self.max_win_time = conf.getint('watchdog', 'max_win_time')
        self.mitama_team_mark = conf.getint('mitama', 'mitama_team_mark')
        self.max_times = conf.getint('DEFAULT', 'max_times')
        self.end_operation = conf.getint('DEFAULT', 'end_operation')
        self.run_times = 0

        # Startup log
        self.log = MyLog.mlogger

        # Bound window
        if hwnd == 0:
            if self.client == 0:
                hwnd = win32gui.FindWindow(0, u'Onmyoji')
            elif self.client == 1:
                hwnd = win32gui.FindWindow(0, u'Onmyoji-Simulator')
                # TansuoPos.InitPosWithClient__()
                # YuhunPos.InitPosWithClient__()
        self.yys = GameControl(hwnd, quit_game_enable)
        self.log.info('Bind the window successfully')
        self.log.info(str(hwnd))

        # Activate window
        self.yys.activate_window()
        self.log.info('Activate the window successfully')
        time.sleep(0.5)

        # Binding scene

        # Self-check
        debug_enable = conf.getboolean('others', 'debug_enable')
        if debug_enable:
            task = threading.Thread(target=self.yys.debug)
            task.start()

    def check_battle(self):
        # Check whether to enter the battle
        self.log.info('Check whether to enter the battle')
        self.yys.wait_game_img('img\\ZI-DONG.png', self.max_win_time)
        self.log.info('Has entered the battle')

    def check_end(self):
        '''
        Check whether it is finished
             :return: The victory page returns 0; the reward page returns 1
        '''
        self.log.info('The test is whether the battle is over')
        start_time = time.time()
        myend = -1
        while time.time()-start_time <= self.max_win_time and self.run:
            # Refuse to offer a reward
            self.yys.rejectbounty()

            maxVal, maxLoc = self.yys.find_multi_img(
                'img/SHENG-LI.png', 'img/TIAO-DAN.png', 'img/JIN-BI.png', 'img/JIE-SU.png')
            end_cof = max(maxVal)
            if end_cof > 0.9:
                myend = maxVal.index(end_cof)
                break
            time.sleep(0.5)
        if myend in [0, 3]:
            self.log.info('Successful battle')
            return 0
        elif myend in [1, 2]:
            self.log.info('End of this round of battle')
            return 1

    def check_times(self):
        '''
        Monitor whether the number of games reaches the maximum number of times
        '''
        self.run_times = self.run_times + 1
        self.log.info('Game is running'+str(self.run_times)+'Times')
        if(self.run_times == self.max_times):
            if(self.end_operation == 0):
                self.log.warning('Close script (the number of times is full)...')
                self.run = False
                os._exit(0)
            elif(self.end_operation == 1):
                self.log.warning('Close the game (the number is full)...')
                self.yys.quit_game()
                self.log.warning('Close script (the number of times is full)...')
                self.run = False
                os._exit(0)

    def get_reward(self, mood, state):
        '''
        Settlement processing
             :param mood: state function
             :param state: The state of the previous step. 0-Successful battle page; 1-Receive reward page
        '''
        # Initialize the settlement point
        mypos = ut.secondposition()
        if state == 0:
            self.yys.mouse_click_bg(mypos)
            self.log.info('Click to check out')
            mood.moodsleep()
        start_time = time.time()
        while time.time()-start_time <= self.max_op_time and self.run:
            # Refuse to offer a reward
            self.yys.rejectbounty()

            while True:
                newpos = (mypos[0] + random.randint(-50, 50),
                          mypos[1] + random.randint(-50, 50))
                if ut.checkposition(newpos):
                    mypos = newpos
                    break

            # Click once to settle
            self.yys.mouse_click_bg(mypos)
            self.log.info('Click to check out')
            mood.moodsleep()

            # Error correction
            maxVal, maxLoc = self.yys.find_multi_img(
                'img/FA-SONG-XIAO-XI.png', 'img/ZHI-LIAO-LIANG.png')
            if max(maxVal) > 0.9:
                self.yys.mouse_click_bg((35, 295), (140, 475))
                self.log.info('Error correction')
                mood.moodsleep()
                continue

            # Normal settlement
            maxVal, maxLoc = self.yys.find_multi_img(
                'img/SHENG-LI.png', 'img/TIAO-DAN.png', 'img/JIN-BI.png', 'img/JIE-SU.png')
            if max(maxVal) < 0.9:
                self.log.info('Settled successfully')
                return

        self.log.warning('Click to check out failed!')
        # Remind the player to fail to click and exit after 5s
        self.yys.activate_window()
        time.sleep(5)
        self.yys.quit_game()

    def mitama_team_click(self):
        '''
        Soul marks one's own way god
        '''
        num = self.mitama_team_mark
        if num > 0:
            # 100 1040
            # 125 50
            # Obtain the marked location in the Royal Soul scene
            min = (num - 1) * 105 + (num - 1) * 100 + 95
            max = min + 50
            pos = (min, 355), (max, 425)

            start_time = time.time()
            while time.time() - start_time <= 3:
                x1 = pos[0][0] - 100
                y1 = pos[0][1] - 250
                x2 = pos[1][0] + 100
                y2 = pos[1][1]
                exp_pos = self.yys.find_color(
                    ((x1, y1), (x2, y2)), (134, 227, 96), 5)
                # print('Color position', exp_pos)
                if exp_pos != -1:
                    self.log.info('Mark Shikigami success')
                    return True
                else:
                    # Click on the designated location and wait for the next round
                    self.yys.mouse_click_bg(*pos)
                    self.log.info('Mark shikigami')
                    ut.mysleep(500)

            self.log.warning('Mark Shikigami failure')

    def click_monster(self):
        # Click on the monster
        pass

    def click_until(self, tag, img_path, pos, pos_end=None, step_time=0.8, appear=True):
        '''
        In a certain period of time, click the mouse in the background until a certain picture appears or disappears
             :param tag: key name
             :param img_path: image path
             :param pos: (x,y) the coordinates of the mouse click
             :param pos_end=None: (x,y) If pos_end is not empty, click the random position in the area where pos is the upper left corner coordinate and pos_end is the lower right corner coordinate
             :step_time=0.5: query interval
             :appear: The picture appears or disappears: Ture-appears; False-disappears
             :return: Return True if successful, exit the game if failed
        '''
        # Repeatedly monitor the screen within the specified time and click
        start_time = time.time()
        while time.time()-start_time <= self.max_op_time and self.run:
            # Click to specify location
            self.yys.mouse_click_bg(pos, pos_end)
            self.log.info('Click on ' + tag)
            ut.mysleep(step_time*1000)

            result = self.yys.find_game_img(img_path)
            if not appear:
                result = not result
            if result:
                self.log.info('Click on ' + tag + ' success')
                return True

        # Remind the player to fail to click and exit after 5s
        self.click_failed(tag)

    def click_until_multi(self, tag, *img_path, pos, pos_end=None, step_time=0.8):
        '''
        In a certain period of time, click the mouse in the background until any picture in the list appears
             :param tag: key name
             :param img_path: image path
             :param pos: (x,y) the coordinates of the mouse click
             :param pos_end=None: (x,y) If pos_end is not empty, click the random position in the area where pos is the upper left corner coordinate and pos_end is the lower right corner coordinate
             :step_time=0.5: query interval
             :return: Return True if successful, exit the game if failed
        '''
        # Repeatedly monitor the screen within the specified time and click
        start_time = time.time()
        while time.time()-start_time <= self.max_op_time and self.run:
            # Click to specify location
            self.yys.mouse_click_bg(pos, pos_end)
            self.log.info('Click on ' + tag)
            ut.mysleep(step_time*1000)

            maxval, _ = self.yys.find_multi_img(*img_path)
            if max(maxval) > 0.9:
                self.log.info('Click on ' + tag + ' success')
                return True

        # Remind the player to fail to click and exit after 5s
        self.click_failed(tag)

    def click_until_knn(self, tag, img_path, pos, pos_end=None, step_time=0.8, appear=True, thread=0):
        '''
        In a certain period of time, click the mouse in the background until a certain picture appears or disappears
             :param tag: key name
             :param img_path: image path
             :param pos: (x,y) the coordinates of the mouse click
             :param pos_end=None: (x,y) If pos_end is not empty, click the random position in the area where pos is the upper left corner coordinate and pos_end is the lower right corner coordinate
             :step_time=0.5: query interval
             :appear: The picture appears or disappears: Ture-appears; False-disappears
             :thread: detection threshold
             :return: Return True if successful, exit the game if failed
        '''
        # Repeatedly monitor the screen within the specified time and click
        start_time = time.time()
        while time.time()-start_time <= self.max_op_time and self.run:
            # Click on the designated location and wait for the next round
            self.yys.mouse_click_bg(pos, pos_end)
            self.log.info('Click on ' + tag)
            ut.mysleep(step_time*1000)

            result = self.yys.find_game_img_knn(img_path, thread=thread)
            if not appear:
                result = not result
            if result:
                self.log.info('Click on ' + tag + ' success')
                return True

        # Remind the player to fail to click and exit after 5s
        self.click_failed(tag)

    def click_failed(self, tag):
        # Remind the player to fail to click and exit after 5s
        self.log.warning('Click on ' + tag + ' failure!')
        self.yys.activate_window()
        time.sleep(5)
        self.yys.quit_game()

    def activate(self):
        self.log.warning('Startup script')
        self.run = True
        self.yys.run = True

    def deactivate(self):
        self.log.warning('Manually stop the script')
        self.run = False
        self.yys.run = False

    def slide_x_scene(self, distance):
        '''
        Horizontal sliding scene
             :return: Return True if successful; Return False if failed
        '''
        x0 = random.randint(distance + 10, 1126)
        x1 = x0 - distance
        y0 = random.randint(436, 486)
        y1 = random.randint(436, 486)
        self.yys.mouse_drag_bg((x0, y0), (x1, y1))
        self.log.info('Horizontal sliding interface')
