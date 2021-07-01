from gameLib.image_proc import match_img_knn
import configparser
import ctypes
import logging
import os
import sys
import time
import traceback
import random
import cv2
import numpy as np
import win32api
import win32con
import win32gui
import win32ui
from PIL import Image


class GameControl():
    def __init__(self, hwnd, quit_game_enable=1):
        '''
        initialization
             :param hwnd: window handle to be bound
             :param quit_game_enable: Whether to quit the game when the program dies. True is yes, False is no
        '''
        self.run = True
        self.hwnd = hwnd
        self.quit_game_enable = quit_game_enable
        self.debug_enable = False
        l1, t1, r1, b1 = win32gui.GetWindowRect(self.hwnd)
        #print(l1,t1, r1,b1)
        l2, t2, r2, b2 = win32gui.GetClientRect(self.hwnd)
        # print(l2,t2,r2,b2)
        self._client_h = b2 - t2
        self._client_w = r2 - l2
        self._border_l = ((r1 - l1) - (r2 - l2)) // 2
        self._border_t = ((b1 - t1) - (b2 - t2)) - self._border_l
        conf = configparser.ConfigParser()
        conf.read('conf.ini')
        self.client = conf.getint('DEFAULT', 'client')
        if self.client == 1:
            os.system('adb connect 127.0.0.1:7555')
            os.system('adb devices')

    def init_mem(self):
        self.hwindc = win32gui.GetWindowDC(self.hwnd)
        self.srcdc = win32ui.CreateDCFromHandle(self.hwindc)
        self.memdc = self.srcdc.CreateCompatibleDC()
        self.bmp = win32ui.CreateBitmap()
        self.bmp.CreateCompatibleBitmap(
            self.srcdc, self._client_w, self._client_h)
        self.memdc.SelectObject(self.bmp)

    def window_full_shot(self, file_name=None, gray=0):
        """
        Window screenshot
             :param file_name=None: save name of the screenshot file
             :param gray=0: whether to return a grayscale image, 0: return a BGR color image, others: return a grayscale black and white image
             :return: return RGB data if file_name is empty
        """
        try:
            if (not hasattr(self, 'memdc')):
                self.init_mem()
            if self.client == 0:
                self.memdc.BitBlt((0, 0), (self._client_w, self._client_h), self.srcdc,
                                  (self._border_l, self._border_t), win32con.SRCCOPY)
            else:
                self.memdc.BitBlt((0, -35), (self._client_w, self._client_h), self.srcdc,
                                  (self._border_l, self._border_t), win32con.SRCCOPY)
            if file_name != None:
                self.bmp.SaveBitmapFile(self.memdc, file_name)
                return
            else:
                signedIntsArray = self.bmp.GetBitmapBits(True)
                img = np.fromstring(signedIntsArray, dtype='uint8')
                img.shape = (self._client_h, self._client_w, 4)
                #cv2.imshow("image", cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))
                # cv2.waitKey(0)
                if gray == 0:
                    return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                else:
                    return cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        except Exception:
            self.init_mem()
            logging.warning('window_full_shot execution failed')
            a = traceback.format_exc()
            logging.warning(a)

    def window_part_shot(self, pos1, pos2, file_name=None, gray=0):
        """
        Screenshot of window area
             :param pos1: (x,y) The coordinates of the upper left corner of the screenshot area
             :param pos2: (x,y) The coordinates of the lower right corner of the screenshot area
             :param file_name=None: The save path of the screenshot file
             :param gray=0: whether to return a grayscale image, 0: return a BGR color image, others: return a grayscale black and white image
             :return: return RGB data if file_name is empty
        """
        w = pos2[0]-pos1[0]
        h = pos2[1]-pos1[1]
        hwindc = win32gui.GetWindowDC(self.hwnd)
        srcdc = win32ui.CreateDCFromHandle(hwindc)
        memdc = srcdc.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(srcdc, w, h)
        memdc.SelectObject(bmp)
        if self.client == 0:
            memdc.BitBlt((0, 0), (w, h), srcdc,
                         (pos1[0]+self._border_l, pos1[1]+self._border_t), win32con.SRCCOPY)
        else:
            memdc.BitBlt((0, -35), (w, h), srcdc,
                         (pos1[0]+self._border_l, pos1[1]+self._border_t), win32con.SRCCOPY)
        if file_name != None:
            bmp.SaveBitmapFile(memdc, file_name)
            srcdc.DeleteDC()
            memdc.DeleteDC()
            win32gui.ReleaseDC(self.hwnd, hwindc)
            win32gui.DeleteObject(bmp.GetHandle())
            return
        else:
            signedIntsArray = bmp.GetBitmapBits(True)
            img = np.fromstring(signedIntsArray, dtype='uint8')
            img.shape = (h, w, 4)
            srcdc.DeleteDC()
            memdc.DeleteDC()
            win32gui.ReleaseDC(self.hwnd, hwindc)
            win32gui.DeleteObject(bmp.GetHandle())
            #cv2.imshow("image", cv2.cvtColor(img, cv2.COLOR_BGRA2BGR))
            # cv2.waitKey(0)
            if gray == 0:
                return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            else:
                return cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

    def find_color(self, region, color, tolerance=0):
        """
        Looking for color
             :param region: ((x1,y1),(x2,y2)) The coordinates of the upper left corner and the lower right corner of the search area
             :param color: (r,g,b) the color to be searched
             :param tolerance=0: tolerance value
             :return: Returns the client area coordinates successfully, returns -1 on failure
        """
        img = Image.fromarray(self.window_part_shot(
            region[0], region[1]), 'RGB')
        width, height = img.size
        r1, g1, b1 = color[:3]
        for x in range(width):
            for y in range(height):
                try:
                    pixel = img.getpixel((x, y))
                    r2, g2, b2 = pixel[:3]
                    if abs(r1-r2) <= tolerance and abs(g1-g2) <= tolerance and abs(b1-b2) <= tolerance:
                        return x+region[0][0], y+region[0][1]
                except Exception:
                    logging.warning('find_color failed to execute')
                    a = traceback.format_exc()
                    logging.warning(a)
                    return -1
        return -1

    def check_color(self, pos, color, tolerance=0):
        """
        Compare the color of a point in the window
             :param pos: (x,y) the coordinates to be compared
             :param color: (r,g,b) the color to be compared
             :param tolerance=0: tolerance value
             :return: Return True for success, False for failure
        """
        img = Image.fromarray(self.window_full_shot(), 'RGB')
        r1, g1, b1 = color[:3]
        r2, g2, b2 = img.getpixel(pos)[:3]
        if abs(r1-r2) <= tolerance and abs(g1-g2) <= tolerance and abs(b1-b2) <= tolerance:
            return True
        else:
            return False

    def find_img(self, img_template_path, part=0, pos1=None, pos2=None, gray=0):
        """
        Find pictures
             :param img_template_path: the path of the image to find
             :param part=0: Whether to search in full screen, 1 is no, others are yes
             :param pos1=None: The coordinates of the upper left corner of the range to be found
             :param pos2=None: The coordinates of the lower right corner of the range to be found
             :param gray=0: Whether to search in color, 0: search for color pictures, 1: search for black and white pictures
             :return: (maxVal,maxLoc) maxVal is the correlation, the closer to 1, the better, maxLoc is the obtained coordinates
        """
        # Take screenshot
        if part == 1:
            img_src = self.window_part_shot(pos1, pos2, None, gray)
        else:
            img_src = self.window_full_shot(None, gray)

        # show_img(img_src)

        # Read file
        if gray == 0:
            img_template = cv2.imread(img_template_path, cv2.IMREAD_COLOR)
        else:
            img_template = cv2.imread(img_template_path, cv2.IMREAD_GRAYSCALE)

        try:
            res = cv2.matchTemplate(
                img_src, img_template, cv2.TM_CCOEFF_NORMED)
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
            # print(maxLoc)
            return maxVal, maxLoc
        except Exception:
            logging.warning('find_img execution failed')
            a = traceback.format_exc()
            logging.warning(a)
            return 0, 0

    def find_img_knn(self, img_template_path, part=0, pos1=None, pos2=None, gray=0, thread=0):
        """
        Find pictures, knn algorithm
             :param img_template_path: the path of the image to find
             :param part=0: Whether to search in full screen, 1 is no, others are yes
             :param pos1=None: The coordinates of the upper left corner of the range to be found
             :param pos2=None: The coordinates of the lower right corner of the range to be found
             :param gray=0: Whether to search in color, 0: search for color pictures, 1: search for black and white pictures
             :return: coordinates (x, y), return (0, 0) if not found, return -1 if failed
        """
        # Take screenshot
        if part == 1:
            img_src = self.window_part_shot(pos1, pos2, None, gray)
        else:
            img_src = self.window_full_shot(None, gray)

        # show_img(img_src)

        # Read file
        if gray == 0:
            img_template = cv2.imread(img_template_path, cv2.IMREAD_COLOR)
        else:
            img_template = cv2.imread(img_template_path, cv2.IMREAD_GRAYSCALE)

        try:
            maxLoc = match_img_knn(img_template, img_src, thread)
            # print(maxLoc)
            return maxLoc
        except Exception:
            logging.warning('find_img_knn failed to execute')
            a = traceback.format_exc()
            logging.warning(a)
            return -1

    def find_multi_img(self, *img_template_path, part=0, pos1=None, pos2=None, gray=0):
        """
        Find multiple pictures
             :param img_template_path: list of image path to find
             :param part=0: Whether to search in full screen, 1 is no, others are yes
             :param pos1=None: The coordinates of the upper left corner of the range to be found
             :param pos2=None: The coordinates of the lower right corner of the range to be found
             :param gray=0: Whether to search in color, 0: search for color pictures, 1: search for black and white pictures
             :return: (maxVal,maxLoc) maxVal is a list of correlations, the closer to 1, the better, maxLoc is the list of obtained coordinates
        """
        # Window screenshot
        if part == 1:
            img_src = self.window_part_shot(pos1, pos2, None, gray)
        else:
            img_src = self.window_full_shot(None, gray)

        # Return value list
        maxVal_list = []
        maxLoc_list = []
        for item in img_template_path:
            # Read file
            if gray == 0:
                img_template = cv2.imread(item, cv2.IMREAD_COLOR)
            else:
                img_template = cv2.imread(item, cv2.IMREAD_GRAYSCALE)

            # Start to recognize
            try:
                res = cv2.matchTemplate(
                    img_src, img_template, cv2.TM_CCOEFF_NORMED)
                minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
                maxVal_list.append(maxVal)
                maxLoc_list.append(maxLoc)
            except Exception:
                logging.warning('find_multi_img failed to execute')
                a = traceback.format_exc()
                logging.warning(a)
                maxVal_list.append(0)
                maxLoc_list.append(0)
        # Back to list
        return maxVal_list, maxLoc_list

    def activate_window(self):
        user32 = ctypes.WinDLL('user32.dll')
        user32.SwitchToThisWindow(self.hwnd, True)

    def mouse_move(self, pos, pos_end=None):
        """
        Simulate mouse movement
             :param pos: (x,y) the coordinates of the mouse movement
             :param pos_end=None: (x,y) If pos_end is not empty, the mouse will move to a random position in the area where pos is the upper-left coordinate and pos_end is the lower-right coordinate
        """
        pos2 = win32gui.ClientToScreen(self.hwnd, pos)
        if pos_end == None:
            win32api.SetCursorPos(pos2)
        else:
            pos_end2 = win32gui.ClientToScreen(self.hwnd, pos_end)
            pos_rand = (random.randint(
                pos2[0], pos_end2[0]), random.randint(pos2[1], pos_end2[1]))
            win32api.SetCursorPos(pos_rand)

    def mouse_click(self):
        """
        Mouse click
        """
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(random.randint(20, 80)/1000)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def mouse_drag(self, pos1, pos2):
        """
        Mouse drag
             :param pos1: (x,y) starting point coordinates
             :param pos2: (x,y) End point coordinates
        """
        pos1_s = win32gui.ClientToScreen(self.hwnd, pos1)
        pos2_s = win32gui.ClientToScreen(self.hwnd, pos2)
        screen_x = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        screen_y = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        start_x = pos1_s[0]*65535//screen_x
        start_y = pos1_s[1]*65535//screen_y
        dst_x = pos2_s[0]*65535//screen_x
        dst_y = pos2_s[1]*65535//screen_y
        move_x = np.linspace(start_x, dst_x, num=20, endpoint=True)[0:]
        move_y = np.linspace(start_y, dst_y, num=20, endpoint=True)[0:]
        self.mouse_move(pos1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        for i in range(20):
            x = int(round(move_x[i]))
            y = int(round(move_y[i]))
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE |
                                 win32con.MOUSEEVENTF_ABSOLUTE, x, y, 0, 0)
            time.sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def mouse_click_bg(self, pos, pos_end=None):
        """
        Background mouse click
             :param pos: (x,y) the coordinates of the mouse click
             :param pos_end=None: (x,y) If pos_end is not empty, click the random position in the area where pos is the upper left corner coordinate and pos_end is the lower right corner coordinate
        """
        if self.debug_enable:
            img = self.window_full_shot()
            self.img = cv2.rectangle(img, pos, pos_end, (0, 255, 0), 3)

        if pos_end == None:
            pos_rand = pos
        else:
            pos_rand = (random.randint(
                pos[0], pos_end[0]), random.randint(pos[1], pos_end[1]))
        if self.client == 0:
            win32gui.SendMessage(self.hwnd, win32con.WM_MOUSEMOVE,
                                 0, win32api.MAKELONG(pos_rand[0], pos_rand[1]))
            win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN,
                                 0, win32api.MAKELONG(pos_rand[0], pos_rand[1]))
            time.sleep(random.randint(20, 80)/1000)
            win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONUP,
                                 0, win32api.MAKELONG(pos_rand[0], pos_rand[1]))
        else:
            command = str(pos_rand[0]) + ' ' + str(pos_rand[1])
            os.system('adb shell input tap ' + command)

    def mouse_drag_bg(self, pos1, pos2):
        """
        Background mouse drag
             :param pos1: (x,y) starting point coordinates
             :param pos2: (x,y) End point coordinates
        """
        if self.client == 0:
            move_x = np.linspace(pos1[0], pos2[0], num=20, endpoint=True)[0:]
            move_y = np.linspace(pos1[1], pos2[1], num=20, endpoint=True)[0:]
            win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN,
                                 0, win32api.MAKELONG(pos1[0], pos1[1]))
            for i in range(20):
                x = int(round(move_x[i]))
                y = int(round(move_y[i]))
                win32gui.SendMessage(
                    self.hwnd, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x, y))
                time.sleep(0.01)
            win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONUP,
                                 0, win32api.MAKELONG(pos2[0], pos2[1]))
        else:
            command = str(pos1[0])+' ' + str(pos1[1]) + \
                ' '+str(pos2[0])+' '+str(pos2[1])
            os.system('adb shell input swipe '+command)

    def wait_game_img(self, img_path, max_time=100, quit=True):
        """
        Waiting for game image
             :param img_path: image path
             :param max_time=60: timeout
             :param quit=True: whether to quit after timeout
             :return: Returns the coordinates on success, returns False on failure
        """
        self.rejectbounty()
        start_time = time.time()
        while time.time()-start_time <= max_time and self.run:
            maxVal, maxLoc = self.find_img(img_path)
            if maxVal > 0.9:
                return maxLoc
            if max_time > 5:
                time.sleep(1)
            else:
                time.sleep(0.1)
        if quit:
            # Quit the game when timed out
            self.quit_game()
        else:
            return False

    def wait_game_img_knn(self, img_path, max_time=100, quit=True, thread=0):
        """
       Waiting for game image
             :param img_path: image path
             :param max_time=60: timeout
             :param quit=True: whether to quit after timeout
             :return: Returns the coordinates on success, returns False on failure
        """
        self.rejectbounty()
        start_time = time.time()
        while time.time()-start_time <= max_time and self.run:
            maxLoc = self.find_img_knn(img_path, thread=thread)
            if maxLoc != (0, 0):
                return maxLoc
            if max_time > 5:
                time.sleep(1)
            else:
                time.sleep(0.1)
        if quit:
            # Quit the game when timed out
            self.quit_game()
        else:
            return False

    def wait_game_color(self, region, color, tolerance=0, max_time=60, quit=True):
        """
        Waiting for game color
             :param region: ((x1,y1),(x2,y2)) the region to search
             :param color: (r,g,b) the color to wait for
             :param tolerance=0: tolerance value
             :param max_time=30: timeout
             :param quit=True: whether to quit after timeout
             :return: Return True for success, False for failure
        """
        self.rejectbounty()
        start_time = time.time()
        while time.time()-start_time <= max_time and self.run:
            pos = self.find_color(region, color)
            if pos != -1:
                return True
            time.sleep(1)
        if quit:
            # Quit the game when timed out
            self.quit_game()
        else:
            return False

    def quit_game(self):
        """
        exit the game
        """
        self.takescreenshot()  # Save the scene
        self.clean_mem()    # Clean up memory
        if not self.run:
            return False
        if self.quit_game_enable:
            if self.client == 0:
                win32gui.SendMessage(
                    self.hwnd, win32con.WM_DESTROY, 0, 0)  # exit the game
            else:
                os.system(
                    'adb shell am force-stop com.netease.onmyoji.netease_simulator')
        logging.info('Exit and finally show that it has been saved to/img/screenshots_folder')
        sys.exit(0)

    def takescreenshot(self):
        '''
        Screenshots
        '''
        name = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        img_src_path = 'img/screenshots/%s.png' %(name)
        self.window_full_shot(img_src_path)
        logging.info('The screenshot has been saved to img/screenshots/%s.png' %(name))

    def rejectbounty(self):
        '''
        Refuse to offer a reward
             :return: Return True if rejected successfully, False otherwise
        '''
        maxVal, maxLoc = self.find_img('img\\XUAN-SHANG.png')
        if maxVal > 0.9:
            self.mouse_click_bg((757, 460))
            return True
        return False

    def find_game_img(self, img_path, part=0, pos1=None, pos2=None, gray=0, thread=0.9):
        '''
        Find pictures
             :param img_path: find path
             :param part=0: Whether to search in full screen, 0 means no, other means yes
             :param pos1=None: The coordinates of the upper left corner of the range to be found
             :param pos2=None: The coordinates of the lower right corner of the range to be found
             :param gray=0: whether to find black and white pictures, 0: find color pictures, 1: find black and white pictures
             :param thread=0.9: custom threshold
             :return: Return the position coordinates if the search succeeds, otherwise it returns False
        '''
        self.rejectbounty()
        maxVal, maxLoc = self.find_img(img_path, part, pos1, pos2, gray)
        # print(maxVal)
        if maxVal > thread:
            return maxLoc
        else:
            return False

    def find_game_img_knn(self, img_path, part=0, pos1=None, pos2=None, gray=0, thread=0):
        '''
        Find pictures
             :param img_path: find path
             :param part=0: Whether to search in full screen, 0 means no, other means yes
             :param pos1=None: The coordinates of the upper left corner of the range to be found
             :param pos2=None: The coordinates of the lower right corner of the range to be found
             :param gray=0: whether to find black and white pictures, 0: find color pictures, 1: find black and white pictures
             :param thread=0:
             :return: Return the position coordinates if the search succeeds, otherwise it returns False
        '''
        self.rejectbounty()
        maxLoc = self.find_img_knn(img_path, part, pos1, pos2, gray, thread)
        # print(maxVal)
        if maxLoc != (0, 0):
            return maxLoc
        else:
            return False

    def debug(self):
        '''
        Self-check resolution and click range
        '''
        # Turn on self-test
        self.debug_enable = True

        # Resolution
        self.img = self.window_full_shot()
        logging.info('Game resolution:' + str(self.img.shape))

        while(1):
            # Click on the range marker
            cv2.imshow('Click Area (Press \'q\' to exit)', self.img)

            # Candidate picture

            k = cv2.waitKey(1) & 0xFF
            if k == ord('q'):
                break

        cv2.destroyAllWindows()
        self.debug_enable = False

    def clean_mem(self):
        '''
        Clean up memory
        '''
        self.srcdc.DeleteDC()
        self.memdc.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, self.hwindc)
        win32gui.DeleteObject(self.bmp.GetHandle())

# For testing


def show_img(img):
    cv2.imshow("image", img)
    cv2.waitKey(0)


def main():
    hwnd = win32gui.FindWindow(0, u'Onmyoji')
    yys = GameControl(hwnd, 0)
    yys.debug()


if __name__ == '__main__':
    main()
