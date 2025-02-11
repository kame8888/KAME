import multiprocessing as mp

import centerCam
import frontCam

#----------------------------------------------------------
if __name__ == '__main__':
    print('start')
    p1 = mp.Process(target=centerCam.centerCam)
    p2 = mp.Process(target=frontCam.frontCam）
    p1.start()
    p2.start(）
