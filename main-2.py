import multiprocessing as mp

import centerCam
import frontCam
import controller

#----------------------------------------------------------
if __name__ == '__main__':
    print('start')
    p1 = mp.Process(target=centerCam.centerCam)
    p2 = mp.Process(target=frontCam.frontCam)
    p3 = mp.Process(target=controller.control)
    p1.start()
    p2.start()
    p3.start()