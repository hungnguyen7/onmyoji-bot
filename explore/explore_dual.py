from gameLib.game_ctl import GameControl
from explore.explore_leader import ExploreLeader
from explore.explore_passenger import ExplorePassenger

import logging
import threading
import win32gui

hwndlist = []


def get_all_hwnd(hwnd, mouse):
    '''
    Get all Onmyoji windows
    '''
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        if win32gui.GetWindowText(hwnd) == u'Onmyoji-NetEase Games':
            hwndlist.append(hwnd)


def get_game_hwnd():
    win32gui.EnumWindows(get_all_hwnd, 0)


class ExploreDual():
    def __init__(self):
        # Initialize window information
        get_game_hwnd()
        self.hwndlist = hwndlist

        # Check whether the window information is correct
        num = len(self.hwndlist)
        if num == 2:
            logging.info('Two windows are detected, and the window information is normal')
        else:
            logging.warning('detected'+str(num)+'Windows, the window information is abnormal!')

        # Initialize drivers and thugs
        for hwnd in hwndlist:
            yys = GameControl(hwnd)
            if yys.find_game_img('img/DUI.png', 1, (68, 242), (135, 306), thread=0.8):
                self.driver = ExploreLeader(hwnd=hwnd, delay=True)
                hwndlist.remove(hwnd)
                logging.info('Captain Discovery')
                break
        self.passenger = ExplorePassenger(hwnd=hwndlist[0])
        logging.info('Passengers found')

    def start(self):
        task1 = threading.Thread(target=self.driver.start)
        task2 = threading.Thread(target=self.passenger.start)
        task1.start()
        task2.start()

        task1.join()
        task2.join()

    def deactivate(self):
        self.hwndlist = []
        self.driver.deactivate()
        self.passenger.deactivate()
