import cv2

def frontCam():
    #外部カメラ設定
    front_cam = cv2.VideoCapture(1) # type: ignore
    #変数初期設定
    vx,vy,x,y = 0,0,0,0
    while True:
        #カメラ画像読み取り
        _, frame_f = front_cam.read()
        #画像を縮小
        img_f = cv2.resize(frame_f,None,None,1.5,1.5) # type: ignore      #画像をグレースケールにする
        gray = cv2.cvtColor(img_f,cv2.COLOR_BGR2GRAY) # type: ignore
        #ぼかしを入れてエッジ検出のノイズを減らす
        blur = cv2.blur(gray,(5,5)) # type: ignore
       #しきい値処理で白黒画像で表現する。
        _,filter2 = cv2.threshold(blur,75,255,cv2.THRESH_BINARY) # type: ignore
        #白黒反転する
        filter2 = cv2.bitwise_not(filter2) # type: ignore
        #クロージング処理をして分割された部分を一体化する。
        disc2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)) # type: ignore
        close = cv2.morphologyEx(filter2,cv2.MORPH_CLOSE,disc2,iterations=20) # type: ignore
        #cv2.imshow('test',close) # type: ignore
        #検出した部分の輪郭を抽出する
        contours,_ = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # type: ignore
        #輪郭の中心を通る線を計算し、描画する
        if contours:
            _,cols = img_f.shape[:2]
            cnt = contours[0]
            vx,vy,x,y = cv2.fitLine(cnt,cv2.DIST_L2,0,0.01,0.01) # type: ignore
            if vx == 0 or x == 0 or vy == 0:
                left_y = int(y)
                print(left_y)
                #right_y = int(y)
                cv2.line(img_f,(0,left_y),(cols-1,right_y),(0,0,255),5) # type: ignore
                ang = 0
            else:
                left_y = int((-x*vy/vx)+y)
                #print(left_y)
                #error ??? intOverflow
                right_y = int(((cols-x)*vy/vx)+y)
                cv2.line(img_f,(0,left_y),(cols-1,right_y),(0,0,255),5) # type: ignore
                ang = int(vy/vx)
            #print(ang)
        #表示する
        cv2.imshow('front',img_f) # type: ignore
        if cv2.waitKey(1) & 0xFF == ord('q'): # type: ignore
            break
    front_cam.release()
    cv2.destroyAllWindows() # type: ignore