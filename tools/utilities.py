import json
import logging
import random
import time


class Mood:
    '''
    Used to simulate random click frequency, changing the click rule every 5 minutes\n
    energetic: The status is excellent, the click delay is 1-1.5s\n
    joyful: The status is good, the click delay is 1.3-2.1s\n
    normal: The state is normal, the click delay is 1.8-3s\n
    tired: State fatigue, click delay is 2.5-4\n
    exhausted: CHSM，Click delay in 3-5s\n
    '''
    __first_init = True

    def __init__(self, state=5):
        self.lastime = time.time()
        self.state = state
        if Mood.__first_init:
            self.read_config()
            Mood.__first_init = False
        a = random.randint(1, self.state)
        logging.info("Create delay parameter, level: %d", a)
        self.lastmood = Mood.mymood[a]

    def read_config(self):
        try:
            # Read delay configuration
            with open('delay.json', 'r') as f:
                fileObject = f.read()
            jsObj = json.loads(fileObject)
            logging.info('Read the delay configuration file successfully')
            Mood.mymood = {
                1: (jsObj['1'][0], jsObj['1'][1]),
                2: (jsObj['2'][0], jsObj['2'][1]),
                3: (jsObj['3'][0], jsObj['3'][1]),
                4: (jsObj['4'][0], jsObj['4'][1]),
                5: (jsObj['5'][0], jsObj['5'][1])}
        except FileNotFoundError:
            # file not found
            logging.info('Use default delay parameters')
            self.set_default()
        except:
            # Other errors
            logging.warning('Delay configuration file error, use default parameters')
            self.set_default()
        logging.info('Delay parameter: '+str(Mood.mymood))

    def set_default(self):
        '''
        Set default delay parameters
        '''
        Mood.mymood = {
            1: (1000, 500),
            2: (1300, 800),
            3: (1800, 1200),
            4: (2500, 1500),
            5: (3000, 2000)}

    def getmood(self):
        if (time.time() - self.lastime >= 300):
            self.lastime = time.time()
            a = random.randint(1, self.state)
            self.lastmood = Mood.mymood[a]
            logging.info("Modify the delay parameter, level %d", a)
        return self.lastmood

    def moodsleep(self):
        mysleep(*self.getmood())

    def get1mood(self):
        return random.randint(self.getmood()[0], self.getmood()[0] + self.getmood()[1])


def firstposition():
    '''
    Get the click location, deduct the soul part
         :return: return random position coordinates
    '''
    safe_area = {
        1: ((20, 106), (211, 552)),
        2: ((931, 60), (1120, 620))}

    index = random.randint(1, 2)
    return safe_area[index]


def secondposition():
    '''
    Get the click location, deduct the soul part
         :return: return random position coordinates
    '''
    return (random.randint(970, 1111), random.randint(100, 452))


def checkposition(pos):
    '''
    Check calculation location
         :param pos: (x, y) position coordinates
         :return: return True if appropriate, otherwise return False
    '''
    if pos[0] < 1111 and pos[0] > 970:
        if pos[1] < 452 and pos[1] > 100:
            return True
    return False


def mysleep(slpa, slpb=0):
    '''
    randomly sleep for a short time between `slpa` and `slpa + slpb` \n
    because of the legacy reason, slpa and slpb are in millisecond
    '''
    if slpb == 0:
        slp = random.randint(int(0.5*slpa), int(1.5*slpa))
    else:
        slp = random.randint(slpa, slpa+slpb)
    time.sleep(slp/1000)


if __name__ == "__main__":
    mood = Mood()
    print(Mood.mymood)
