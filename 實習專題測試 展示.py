import cv2
import sqlite3
import winsound
cap = cv2.VideoCapture(1)
img_pre = None   # 前影像, 預設是空的
while cap.isOpened():
    success, img = cap.read()
    if success:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)        # 灰階處理
        img_now = cv2.GaussianBlur(gray, (13, 13), 5)       # 高斯模糊
        if img_pre is not None:  # ←如果前影像不是空的, 就和前影像比對
            diff = cv2.absdiff(img_now, img_pre)   # 此影格與前影格的差異值
            ret, thresh = cv2.threshold(diff, 25, 255,  # 門檻值
                                        cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh,    # 找到輪廓
                                           cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)
            if contours:    # 如果有偵測到輪廓
                cv2.drawContours(img, contours, -1, (255, 255, 255), 2)
                print('偵測到移動')
                def getFeature(imgfile):
                    img = dlib.load_rgb_image(imgfile)  #讀取圖片
                    dets = detector(img, 1)
                    for det in dets:
                        shape = sp(img, det)  #特徵點偵測
                        feature = facerec.compute_face_descriptor(img, shape)  #取得128維特徵向量
                        return numpy.array(feature)  #轉換numpy array格式

                def compareimage(v, filepath):  #人臉比對
                    try:
                        v2 = getFeature(filepath)
                        dist = numpy.linalg.norm(v-v2)  # 計算歐式距離,越小越像
                        if dist < 0.3: 
                            return True
                        else:
                            return False
                    except Exception:
                        print("產生錯誤，無法識別！") 
                        winsound.Beep(440, 10000)

                        return 0

                import cv2
                import sqlite3
                import time
                from datetime import datetime
                import dlib, numpy
                from skimage import io

                predictor_path = "model2.dat"  #人臉68特徵點模型
                face_rec_model_path = "model1.dat"  #人臉辨識模型
                detector = dlib.get_frontal_face_detector()  #偵測臉部正面
                sp = dlib.shape_predictor(predictor_path)  #讀入人臉特徵點模型
                facerec = dlib.face_recognition_model_v1(face_rec_model_path)  #讀入人臉辨識模型

                conn = sqlite3.connect('member.sqlite7')  #連接資料庫
                cursor = conn.cursor()
                sqlstr = 'SELECT * FROM member'  #讀取會員資料表
                cursor.execute(sqlstr)
                rows = cursor.fetchall()  #取得會員資料
                imagedict = {}  #會員帳號、檔名字典
                for row in rows:  
                    imagedict[row[0]] = 'memberPic/' + row[1]

                timenow = time.time()  #取得現在時間數值
                cv2.namedWindow("frame")
                cap = cv2.VideoCapture(1)  #開啟cam
                while(cap.isOpened()):  #cam開啟成功
                    count = 5 - int(time.time() - timenow)  #倒數計時5秒
                    ret, img = cap.read()
                    if ret == True:
                        imgcopy = img.copy()  #複製影像
                        cv2.putText(imgcopy, str(count), (200,400), cv2.FONT_HERSHEY_SIMPLEX, 15, (0,0,255), 35)  #在複製影像上畫倒數秒數
                        cv2.imshow("frame", imgcopy)  #顯示複製影像
                        k = cv2.waitKey(100)  #0.1秒讀鍵盤一次
                        if k == ord("z") or k == ord("Z") or count == 0:  #按「Z」鍵或倒數計時結束
                            cv2.imwrite("login/terry.jpg", img)  #將影像存檔
                            break
                cap.release()  #關閉cam
                cv2.destroyWindow("frame")

                success = False  #記錄登入是否成功
                v = getFeature("login/terry.jpg")
                for img in imagedict:  #逐一比對會員圖片
                    if compareimage(v, imagedict[img]):  #判斷為同一人
                        print('登入成功！歡迎 ' + img + '！' )
                        success = True
                        savetime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  #目前時刻字串
                        sqlstr = 'INSERT INTO login values("{}","{}")'.format(img, savetime)  #將帳號及現在時刻寫入資料表
                        cursor.execute(sqlstr)
                        conn.commit()
                        break
                if not success:  #登入失敗
                    winsound.Beep(440, 10000)
                    print('登入失敗！你不是會員！')    
            else:
                print('靜止畫面')


        cv2.imshow('frame', img)
        img_pre = img_now.copy()
    k = cv2.waitKey(50)
    if k == ord('q'):
        cv2.destroyAllWindows()
        cap.release()