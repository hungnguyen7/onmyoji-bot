import logging


class MyLog():
    plogger = logging.getLogger('Passenger')
    dlogger = logging.getLogger('Driver')
    mlogger = logging.getLogger()

    @staticmethod
    def init():
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)-17s [line:%(lineno)-3s] %(levelname)-7s %(name)-9s %(message)s',
                            datefmt='%Y %b %d %H:%M:%S',
                            filename='log.log',
                            filemode='w')

        #################################################################################################
        # Define a StreamHandler, print INFO level or higher log information to standard error, and add it to the current log processing object#
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s   %(filename)-17s: %(levelname)-7s %(name)-9s %(message)s')
        console.setFormatter(formatter)
        MyLog.mlogger.addHandler(console)
        #################################################################################################
