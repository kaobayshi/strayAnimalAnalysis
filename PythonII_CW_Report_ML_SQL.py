# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 14:15:55 2020

@author: miomio-NB
"""
import pandas as pd
import pymssql as db
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

userTag = ['AAAAG', 'AAACG', 'AAADG', 'AAAEG', 'AAAFG', 'AAAGG',
            'AAAHG', 'AAAIG', 'AAAJG', 'BAAAG', 'CAAAG', 'DAAAG',
            'EAAAG', 'FAAAG', 'GAAAG', 'HAAAG', 'IAAAG', 'JAAAG',
            'LAAAG', 'LAABG', 'MAAAG', 'NAAAG', 'OAAAG', 'PAAAG',
            'QAAAG', 'RAAAG', 'TAAAG', 'UAAAG', 'UAABG', 'VAAAG',
            'XAAAG', 'YAAAG']    

userName = ["新北市政府動物保護防疫處", "新北市新店區公立動物之家","新北市板橋區公立動物之家", 
            "新北市中和區公立動物之家", "新北市淡水區公立動物之家", "新北市瑞芳區公立動物之家",
            "新北市五股區公立動物之家", "新北市八里區公立動物之家", "新北市三芝區公立動物之家", 
            "宜蘭縣流浪動物中途之家","桃園市動物保護教育園區", "新竹縣公立動物收容所",
            "苗栗縣生態保育教育中心(動物收容所)", "臺中市動物之家南屯園區", "彰化縣流浪狗中途之家", 
            "南投縣公立動物收容所", "雲林縣流浪動物收容所", "嘉義縣流浪犬中途之家",
            "高雄市壽山動物保護教育園區", "高雄市燕巢動物保護關愛園區", "屏東縣公立犬貓中途之家", 
            "臺東縣動物收容中心","花蓮縣流浪犬中途之家", "澎湖縣流浪動物收容中心",
            "基隆市寵物銀行", "新竹市動物保護教育園區", "嘉義市動物保護教育園區", 
            "臺南市動物之家灣裡站", "臺南市動物之家善化站", "臺北市動物之家",
            "連江縣流浪犬收容中心", "金門縣動物收容中心"]

userTel = ["02-29596353", "02-22159462", "02-89662158", "02-86685547",
            "02-26267558", "02-24063481", "02-82925265", "02-26194428",
            "02-26365436", "039602350 #620", "03-4861760", "03-5519548",
            "037-558228", "04-23850976", "04-8590638", "049-2225440",
            "", "05-2950053", "07-5519059", "07-6051002", "0905-981-077",
            "089-362011", "038-421452", "06-9213559", "02-24560148",
            "03-5368329", "05-2168661", "06-2964439", "06-5832399",
            "02-87913254", "0836-25003", "082-336625"]

userAddr = ["新北市板橋區四川路一段157巷2號", "新北市新店區安泰路235號",
            "新北市板橋區板城路28-1號", "新北市中和區興南路三段100號",
            "新北市淡水區下圭柔山91之3號", "新北市瑞芳區靜安路四段(106縣道74.5K清潔隊場區內)",
            "新北市五股區外寮路9-9號", "新北市八里區長坑里6鄰長坑道路36號",
            "新北市三芝區青山路(龍巖人本旁)", "宜蘭縣五結鄉成興村利寶路60號",
            "桃園市新屋區永興里3鄰藻礁路1668號", "新竹縣竹北市縣政五街192號",
            "苗栗縣銅鑼鄉朝陽村6鄰朝北55-1號", "臺中市南屯區中台路601號",
            "彰化縣員林市大峯里阿寶巷426號(大門入口請由彰化縣芬園鄉大彰路一段875巷進入走到底)",
            "南投縣南投市嶺興路36-1號", "", "嘉義縣大林鎮中坑里中興2-6號",
            "高雄市鼓山區萬壽路350號", "高雄市燕巢區師大路98號",
            "屏東縣內埔鄉學府路1號(屏東科技大學內)", "臺東縣臺東市中華路4段999巷600號",
            "花蓮縣吉安鄉南濱路1段599號", "澎湖縣馬公市烏崁里260號",
            "基隆市七堵區大華三路45-12號(欣欣安樂園旁)", "新竹市南寮里海濱路250號",
            "嘉義市彌陀路31號旁", "臺南市南區省躬里14鄰萬年路580巷92號",
            "臺南市善化區東昌里東勢寮1~19號", "臺北市內湖區潭美街852號",
            "連江縣南竿鄉復興村(近機場)", "金門縣金湖鎮裕民農莊20號"]

usertitle = [20, 170, 347, 353, 85, 100, 260, 160, 120, 270, 652, 114, 220, 400,
              189, 250, 300, 110, 250, 650, 80, 104, 92, 140, 100, 250, 100, 400,
              300, 450, 120, 200]

# 連接資料庫
conn = db.connect(server='127.0.0.1', 
                  user='Elena', 
                  password='1234', 
                  database='PythonReport2_animaldata', 
                  port='1433')
cur = conn.cursor()

# 讀取檔案
data_read = pd.read_sql("SELECT * FROM animal_load", con = conn)

dog = data_read.groupby("classname")
dog = dog.get_group("犬")
# print(dog)

dog.sort_values("indate", inplace = True)

# 機器學習部分_線性回歸(分開收容所，以日期分)
for tag, name, tel, addr, title in zip(userTag, userName, userTel, userAddr, usertitle): 
    xLt = []
    yLt_1 = []
    yLt_2 = []
    df = dog.groupby("asylumnm")
    a = df.get_group(name)
    # print(a)
    b = a.groupby("indate")
    # print(b)
    for i in range(1, len(b)+1):
        xLt.append(i)
    for j in b:
        c = len(j[1])
        yLt_1.append(c)
    sum = 0
    for i in yLt_1:
        sum += i
        yLt_2.append(sum)
    X = pd.DataFrame(xLt, columns = ["date"] )
    y = pd.DataFrame(yLt_2, columns = ["Quantity"] )
    lm = LinearRegression()
    lm.fit(X, y)
    pred = lm.predict(X)
    mse = np.mean((y-pred)**2)
    print(name)
    print("迴歸係數：", lm.coef_)
    print("截距：", lm.intercept_)
    print("MSE：", mse)
    print("R-squared：", lm.score(X, y))
    
    plt.rcParams["font.sans-serif"] = "mingliu" #設定中文字型
    plt.scatter(xLt, yLt_2)
    regression_Quantity = lm.predict(X)
    plt.plot(xLt, regression_Quantity, color = "blue")
    plt.title(name)
    plt.savefig(".\\ML_pic\\" + name + ".jpg")
    # plt.show()
   
    more = 0
    while True:
        new_Date = pd.DataFrame([len(yLt_2) + more])
        new_Quantity = lm.predict(new_Date)
        if new_Quantity[0] < title:
            more += 1
        else:
            if more != 0:
                result = ("{}將於 {} 天後爆滿。".format(name, more))
            else:
                result = ("{}已爆滿。".format(name))
            break
    data = {"asylumTag" : tag,
            "asylumnm" : name,
            "asylumtel" : tel,
            "asylumaddr" : addr,
            "asylumprediction" : result}
    # print(data)
    cur.execute("SELECT * FROM asylum_data WHERE asylumTag=%s", data['asylumTag'])
    isiddata = cur.fetchall()
    if len(isiddata):
        target = str(isiddata[0][0])
        try:
            sql = "UPDATE asylum_data SET asylumprediction='" + data['asylumprediction'] + "' WHERE id=" + target
            cur.execute(sql)
            conn.commit()
            print('已成功修改一筆紀錄：{}'.format(target))
        except Exception as e1:
            conn.rollback()
            print(e1.args)
            print("修改資料失敗：{}".format(isiddata[0]))
    else:
        try:
            cur.executemany(
                    '''INSERT INTO asylum_data(asylumTag, asylumnm, asylumtel, 
                    asylumaddr, asylumprediction) 
                    Values (%s, %s, %s, %s, %s)''',
                    [(data['asylumTag'], data['asylumnm'], data['asylumtel'], 
                      data['asylumaddr'], data['asylumprediction'])]
                            )
    
            conn.commit()
            print('新增一筆紀錄')
        except:
            conn.rollback()
            print('新增記錄失敗...')
            pass

data_read = pd.read_sql("SELECT * FROM asylum_data", con = conn)

data_read.to_csv(".\\animal_asysulm_heroku\\asylum_data_copy.csv", index=False)

cur.close()        
conn.close()



 