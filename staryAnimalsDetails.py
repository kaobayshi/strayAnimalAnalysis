# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 19:10:30 2023

@author: USER
"""

import sqlite3 as db
import requests
import urllib3
import json
import base64
import time
import datetime

# 關閉InsecureRequestWarning顯示
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 連接資料庫
conn = db.connect("staryAnimalData.db")
cur = conn.cursor()
dbData = cur.execute('select * from animalSimpleData')
simpleAnimalDatas = dbData.fetchall()

for simpleAnimalData in simpleAnimalDatas:

    AcNum = simpleAnimalData[0]
    Shelter = simpleAnimalData[2]
    # 欲爬取的全國動物收容資料個別網址
    url = "https://www.pet.gov.tw/handler/AnimalsCore.ashx"
    
    # Request Headers
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}
    # Payload Form Data
    formData = {'Method' : 'AnimalsFront',
                'Param' : '{"action":"AnnounceMentDataDetail","_FrontParam":{"AcNum":"' + AcNum +'","Shelter":"' + Shelter + '","MenuID":2,"PageType":"Adopt"}}'}
    # 傳遞表單並取得資料
    response = requests.post(url = url, headers = headers, data = formData, verify = False)
    # content = 網頁回傳的資料
    content = response.content.decode()
    # contentJson = 將 JSON 物件轉換成為 Python 的資料物件
    contentJson = json.loads(content)
    # contentTarget = 取出特定JSON欄位，這裡的目標欄位是"Message"
    contentTarget = contentJson['Message']
    # contentList = 將contentTarget格式化
    contentList = json.loads(contentTarget)
    # contentDict = 將contentList中的dict取出
    contentDict = contentList[0]
    # print(contentDict)
    
    # 獲取當前日期
    current_dateTime = datetime.datetime.now()
    endDay = str(current_dateTime.year) + "/" + str(current_dateTime.month) + "/" + str(current_dateTime.day)
    # print(endDay)

    
    # 在資料庫中搜尋是否已經有該筆動物資料
    try:
        animalSql = "SELECT isid FROM animalData WHERE isid = '" + AcNum + "'"
        cur.execute(animalSql)
        isAnimalData = cur.fetchall()
        # 如果有的話就印出已收錄然後PASS過該筆資料
        if len(isAnimalData):
            print("Animal：{} 已收錄".format(AcNum))
            continue
        else:
            # 寫入資料庫
            try:
                # 連接資料庫
                detailsData = {'isid' : contentDict['收容編號'], # 資料庫中的編號(等同於收容編號)
                               'indate' : contentDict['入所日期'], # 入所日期
                               'indays' : str(contentDict['入所天數']), # 入所天數
                               'title' : contentDict['收容編號'], # 收容編號
                               'classname' : contentDict['動物類別'], # 動物別(貓、狗...)
                               'variety' : contentDict['品種/物種'], # 動物品種
                               'color' : contentDict['毛色'], # 毛色
                               'area' : contentDict['來源行政區'], # 來源行政區
                               'sex' : contentDict['動物性別'], #char(10) 動物性別編號 1 = 公, 2 = 母, x = 性別不明
                               "endDay" : str(endDay), # 最後能找到該筆資料的那天
                               'asylumnm' : contentDict['公告收容所'], #公告收容所名稱
                               'asylumtel' : contentDict['收容所電話'], # 公告收容所電話
                               'asylumaddr' : contentDict['收容所地址'], #公告收容所地址
                               'isOpen' : contentDict['是否開放認領養'], #是否開放認領養 or 已出所
                               'note' : contentDict['描述'], # 備註描述
                               'photo' : contentDict['img1'], #照片網址
                               'picLocalUrl' : '..\\pic\\' + contentDict['img1'],
                               }
                
                insertSql = "INSERT INTO animalData(isid, indate, indays, title, classname, variety, color, area, sex, endDay, asylumnm, asylumtel, asylumaddr, isOpen, note, photo, picLocalUrl) Values ('" + detailsData['isid'] + "','" + detailsData['indate'] + "','"+ detailsData['indays'] +"', '"+ detailsData['title'] + "', '"+ detailsData['classname'] + "','" + detailsData['variety'] + "','" + detailsData['color'] + "','" + detailsData['area'] + "','" + detailsData['sex'] + "','" + detailsData['endDay'] + "','" + detailsData['asylumnm'] + "','" + detailsData['asylumtel'] + "','" + detailsData['asylumaddr'] + "','" + detailsData['isOpen'] + "','" + detailsData['note'] + "','" + detailsData['photo'] + "','" + detailsData['picLocalUrl'] + "')"
                # print(insertSql)
                cur.execute(insertSql)
                conn.commit()
                print('新增一筆紀錄')
                
            except:
                conn.rollback()
                print('新增記錄失敗...')
                continue
            
    except:
        print("出現錯誤了")
    
    time.sleep(60)

# 關閉資料庫
cur.close()        
conn.close()
time.sleep(60)
print("全國動物收容完整資料下載完畢")
    

