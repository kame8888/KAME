import cv2
import serial

def centerCam():
    #内部カメラ設定
    center_cam = cv2.VideoCapture(0) # type: ignore
    #変数初期設定
    x,y,w,h = 0,0,0,0

    while True:
        #カメラ画像読み取り
        ret1, frame_c = center_cam.read()
        #画像を縮小
        img_c = cv2.resize(frame_c,None,None,1.4,1.4) # type: ignore
        #画像をHSV形式に変換
        hsv_cam = cv2.cvtColor(img_c,cv2.COLOR_RGB2HSV) # type: ignore
        target = cv2.cvtColor(cv2.imread("sample.png"),cv2.COLOR_RGB2HSV) # type: ignore
        #検出する物のヒストグラムを計算
        hist_target = cv2.calcHist([target],[0,1],None,[180, 256],[0,179,0,255]) # type: ignore
        #ヒストグラムを0-255で正規化（データの関係を統一する）
        cv2.normalize(hist_target,hist_target,0,255,cv2.NORM_MINMAX) # type: ignore
        #カメラ画像のそれぞれの画素が確率的に検出する物と対応している画像を生成する
        back_projection = cv2.calcBackProject([hsv_cam],[0,1],hist_target,[0,179,0,255],1) # type: ignore
        #円形カーネルを生成し、線形フィルタリングする
        disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(25,25)) # type: ignore
        cv2.filter2D(back_projection,-1,disc,back_projection) # type: ignore
        #しきい値処理で白黒画像で表現する。
        _,filter = cv2.threshold(back_projection,50,255,0) # type: ignore
        #検出した部分の輪郭を描画する
        contours,_ = cv2.findContours(filter, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # type: ignore
        for i, contour in enumerate(contours):
            x,y,w,h = cv2.boundingRect(contour) # type: ignore
            cv2.rectangle(img_c, (x,y), (x+w-1,y+h-1), (0, 0, 255), 2) # type: ignore
        #面積を計算し、傷口か判別する
        #print(w*h)
        if w*h > 3600:
            b = "check\n"
            #print(b)
            #各スパイクにcheckを送る
            serial1 = serial.Serial(port='/dev/ttyACM0',baudrate=115200)
            serial1.write(b.encode('utf-8'))
            serial1.close()
            #print(b)
            serial2 = serial.Serial(port='/dev/ttyACM1',baudrate=115200)
            serial2.write(b.encode('utf-8'))
            serial2.close()
            w,h = 0,0
        #表示する
        cv2.imshow('center',img_c) # type: ignore
        if cv2.waitKey(1) & 0xFF == ord('q'): # type: ignore
            break
    center_cam.release()
    cv2.destroyAllWindows() # type: ignore