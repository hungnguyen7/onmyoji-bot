from explore.explore import ExploreFight
from explore.explore_passenger import ExplorePassenger
from explore.explore_leader import ExploreLeader
from explore.explore_dual import ExploreDual
from goryou.single_fight import GoryouFight
from mitama.dual import DualFighter
from mitama.fighter_driver import DriverFighter
from mitama.fighter_passenger import FighterPassenger
from mitama.single_fight import SingleFight
from tools.logsystem import MyLog

import configparser
import ctypes
import logging
import os
import sys


def init():
    conf = configparser.ConfigParser()
    # Read configuration file
    conf.read('conf.ini', encoding="utf-8")

    # Set zoom
    # Query DPI Awareness (Windows 10 and 8)
    awareness = ctypes.c_int()
    errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(
        0, ctypes.byref(awareness))

    # Set DPI Awareness  (Windows 10 and 8)
    client = conf.getint('DEFAULT', 'client')
    if client == 0:
        errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(0)
    else:
        errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(1)

    # Read primary copy
    section = conf.getint('DEFAULT', 'run_section')
    # 0 - Soul
    # 1 - Evolve
    # 2 - Exploration
    if section == 0:
        # Soul mode
        mode = conf.getint('DEFAULT', 'run_mode')
        if mode == 0:
            # Single player
            fight = SingleFight()

        elif mode == 1:
            # As a driver, team up with friends and automatically invite
            fight = DriverFighter()

        elif mode == 2:
            # Team up as a passenger and automatically accept the invitation
            fight = FighterPassenger()

        elif mode == 3:
            # Choose when opening 2 game windows on the same computer
            fight = DualFighter()

    elif section == 1:
        # Evolve mode
        fight = GoryouFight()

    elif section == 2:
        # Exploration mode
        mode = conf.getint('explore', 'explore_mode')
        if mode == 0:
            # Single player
            fight = ExploreFight()
        elif mode == 1:
            # As a driver, team up with friends and automatically invite
            fight = ExploreLeader()
        elif mode == 2:
            # Team up as a passenger and automatically accept the invitation
            fight = ExplorePassenger()
        elif mode == 3:
            # Choose when opening 2 game windows on the same computer
            fight = ExploreDual()

    fight.start()


def is_admin():
    # UAC application, get administrator
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def my_excepthook(exc_type, exc_value, tb):
    msg = ' Traceback (most recent call last):\n'
    while tb:
        filename = tb.tb_frame.f_code.co_filename
        name = tb.tb_frame.f_code.co_name
        lineno = tb.tb_lineno
        msg += '   File "%.500s", line %d, in %.500s\n' % (
            filename, lineno, name)
        tb = tb.tb_next

    msg += ' %s: %s\n' % (exc_type.__name__, exc_value)

    logging.error(msg)


if __name__ == "__main__":
    try:
        # Check admin rights
        if is_admin():
            # Initialization log
            MyLog.init()

            # Error message into the log
            sys.excepthook = my_excepthook
            logging.info('UAC pass')

            # Set combat parameters
            init()

        else:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, __file__, None, 1)
    except KeyboardInterrupt:
        logging.info('terminated')
        os._exit(0)
    else:
        pass
