# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 13:44:23 2023

@author: USER
"""

import sqlite3 as db

conn = db.connect("staryAnimalData.db")

cur = conn.cursor()

# 建立動物基本資料表
cur.execute('''CREATE TABLE IF NOT EXISTS animalSimpleData
        (acceptNum TEXT NOT NULL,
        acNum TEXT NOT NULL,
        userTagNum TEXT NOT NULL,
        utNum TEXT NOT NULL,
        animalUrl TEXT NOT NULL)''')
        
# 建立動物詳細資料表
cur.execute('''CREATE TABLE IF NOT EXISTS animalData
        (type INTEGER,
        isid TEXT ,
        indate INTEGER,
        indays INTEGER,
        title TEXT,
        classname TEXT,
        variety TEXT,
        color TEXT,
        area TEXT,
        sex TEXT,
        endDay TEXT,
        asylumnm TEXT,
        asylumtel TEXT,
        asylumaddr TEXT,
        isOpen TEXT,
        note TEXT,
        photo TEXT,
        piclocalurl TEXT)''')
        
# 關閉資料庫
cur.close()        
conn.close()
'''
detailsData = {'type' : int(2), # 該筆資料來源編號(公立收容所為2)
               'isid' : contentDict['收容編號'], # 資料庫中的編號(等同於收容編號)
               'indate' : contentDict['入所日期'], # 入所日期
               'indays' : contentDict['入所天數'], # 入所天數
               'title' : contentDict['收容編號'], # 收容編號
               "inreason" : contentDict['進所原因'], # 進所原因
               'classname' : contentDict['動物類別'], # 動物別(貓、狗...)
               'variety' : contentDict['品種//物種'], # 動物品種
               'color' : contentDict['毛色'], # 毛色
               'area' : contentDict['來源行政區'], # 來源行政區
               'sex' : contentDict['動物性別'], #char(10) 動物性別編號 1 = 公, 2 = 母, x = 性別不明
               'name' : contentDict['動物名'], # 動物名
               "endDay" : str(endDay), # 最後能找到該筆資料的那天
               'asylumnm' : contentDict['公告收容所'], #公告收容所名稱
               'asylumtel' : contentDict['收容所電話'], # 公告收容所電話
               'asylumaddr' : contentDict['收容所地址'], #公告收容所地址
               'note' : contentDict['描述'], # 備註描述
               'photo' : contentDict['img1'], #照片網址
               'picLocalUrl' : '..\\pic\\' + contentDict['img1'],
               }
'''