import sqlite3

conn = sqlite3.connect('member.sqlite7')
cursor = conn.cursor()
sqlstr = 'CREATE TABLE IF NOT EXISTS member("memberid" TEXT, "picture" TEXT)'  #會員資料表
cursor.execute(sqlstr)
sqlstr = 'CREATE TABLE IF NOT EXISTS login("memberid" TEXT, "ltime" TEXT)'  #登入資料表
cursor.execute(sqlstr)
conn.commit()

conn.close()

import cv2
import sqlite3

conn = sqlite3.connect('member.sqlite7')  #連接資料庫
cursor = conn.cursor()
sqlstr = 'SELECT * FROM member'  #讀取會員資料表
cursor.execute(sqlstr)
rows = cursor.fetchall()  #取得會員資料
member = []
for row in rows:  #儲存所有會員帳號
    member.append(row[0])
while True:
    memberid = input('輸入帳號 (直接按「Enter」結束)：')
    if memberid == '':  #未輸入帳號就結束
        break
    elif memberid in member:  #帳號已存在
        print('此帳號已存在，不可重複！')
    else:  #建立帳號
        picfile = memberid + '.jpg'  #會員圖片檔名稱
        member.append(memberid)
        cv2.namedWindow("frame")
        cap = cv2.VideoCapture(1)  #開啟cam
        while(cap.isOpened()):  #如果cam已開啟
            ret, img = cap.read()  #讀取影像
            if ret == True:
                cv2.imshow("frame", img)  #顯示影像
                k = cv2.waitKey(100)  #0.1秒檢查一次按鍵
                if k == ord("z") or k == ord("Z"):  #按下「Z」鍵
                    cv2.imwrite('memberPic/' + picfile, img)  #儲存影像
                    break
        cap.release()  #關閉cam
        cv2.destroyWindow("frame")
        sqlstr = 'INSERT INTO member values("{}","{}")'.format(memberid, picfile)  #將帳號及影像檔名稱寫入資料表
        cursor.execute(sqlstr)
        conn.commit()
        print('帳號建立成功！')

conn.close()