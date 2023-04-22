# 取得人臉特徵點
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
        import sqlite3
        conn = sqlite3.connect('member.sqlite7')  #連接資料庫
        cursor = conn.cursor()
        sqlstr = 'SELECT * FROM login'  #讀取登入資料表
        cursor.execute(sqlstr)
        rows = cursor.fetchall()  #取得登入資料
        print('%-15s %-20s' % ('帳號','登入時間'))
        print('=============== ====================')
        for row in rows:  
            print('%-15s %-20s' % (row[0], row[1]))
        conn.close()
        break
if not success:  #登入失敗
    print('登入失敗！你不是會員！')
conn.close()