# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 23:13:47 2023

@author: USER
"""

import sqlite3 as db
import requests
import urllib3
import json
import base64
import time

# 關閉InsecureRequestWarning顯示
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 連接資料庫
conn = db.connect("staryAnimalData.db")
cur = conn.cursor()

# 欲爬取的全國動物收容資料網址
url = 'https://www.pet.gov.tw/handler/AnimalsCore.ashx'
# Request Headers
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}

# Payload Form Data
formData = {'Method' : 'AnimalsFront',
            'Param' : '{"action":"AnnounceMentData","_FrontParam":{"PageSize":20,"PageNo":"' + '1' + '","AcNum":"","CNum":"","Shelter":"","aType":"","aBreed":"","PageType":"Adopt","PetSex":"","HAIRCOLOR":"","County":"","Age":"","County2":"","DistrictTeam":""}}'}


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

# maxNum = 資料總筆數
maxNum = contentList[0]['MAXNum']
# maxPageNum = 總頁數
if maxNum % 20 != 0: # 如果餘除20不為0，取商數後就多+一頁
    maxPageNum = int((maxNum // 20) + 1)
else: # 如果餘除20為0，那就取商數
    maxPageNum = int(maxNum // 20)

# 取得maxPageNum從頭開始爬取 
for page in range(1, maxPageNum + 1):
    page = str(page)
    print(page)
    # 重新傳輸資料
    # Payload Form Data
    formData = {'Method' : 'AnimalsFront',
                'Param' : '{"action":"AnnounceMentData","_FrontParam":{"PageSize":20,"PageNo":"' + page + '","AcNum":"","CNum":"","Shelter":"","aType":"","aBreed":"","PageType":"Adopt","PetSex":"","HAIRCOLOR":"","County":"","Age":"","County2":"","DistrictTeam":""}}'}

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
    # 取得個別動物資料
    for animalSimpleData in contentList:
        
        # acceptNum = 取得個別動物收容編號
        acceptNum = animalSimpleData['AcceptNum']
        
        # 在資料庫中搜尋是否已經有該筆動物資料
        try:
            animalSql = "SELECT acceptNum FROM animalSimpleData WHERE acceptNum = '" + acceptNum + "'"
            cur.execute(animalSql)
            isAnimalData = cur.fetchall()
            # 如果有的話就印出已收錄然後PASS過該筆資料
            if len(isAnimalData):
                print("Animal：{} 已收錄".format(acceptNum))
                continue
            else:
                # acNum_en = 將收容編號轉為base64 
                acNum_en = base64.b64encode(acceptNum.encode("utf-8"))
                # acNum = 將轉碼後的收容編號轉為字串型態
                acNum = str(acNum_en, "utf-8")
                
                # userTagNum = 取得個別動物UserTag編號
                userTagNum = animalSimpleData['UserTag']
                # userTagNum_en = 將UserTag編號轉為base64
                userTagNum_en = base64.b64encode(userTagNum.encode("utf-8"))
                # utNum = 將轉碼後的userTag編號轉為字串型態
                utNum = str(userTagNum_en, "utf-8")
                
                # 取得個別動物網址備查
                animalUrl = "https://www.pet.gov.tw/AnimalApp/AnnounceSingle.aspx?PageType=Adopt&PG=" + page +"&AcNum=" + acNum + "&UT=" + utNum
                
                # 寫入資料庫
                try:
                    # 連接資料庫
                    dbData = {"acceptNum" : acceptNum,
                              "acNum" : acNum, 
                              "userTagNum" : userTagNum,
                              "utNum" : utNum, 
                              "animalUrl" : animalUrl
                              }
                    insertSql = insertSql = "INSERT INTO animalSimpleData(acceptNum, acNum, userTagNum, utNum, animalUrl) Values ('" + dbData['acceptNum'] + "','" + dbData['acNum'] + "','" + dbData['userTagNum'] + "','"+ dbData['utNum'] +"', '"+ dbData['animalUrl'] + "')"
                    cur.execute(insertSql)
                    conn.commit()
                    print('新增一筆紀錄')
                    
                except:
                    conn.rollback()
                    print('新增記錄失敗...')
                    continue
                
        except:
            print("出現錯誤了")
            
    time.sleep(120)
    
# 關閉資料庫
cur.close()        
conn.close()
time.sleep(60)
print("全國動物收容資料下載完畢")
