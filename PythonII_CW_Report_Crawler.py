# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 16:19:45 2020

@author: miomio-NB
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import datetime
import time
import json
import pymssql as db
import schedule
import pandas as pd

def animal_download():
    # 連線資料庫
    conn = db.connect(server='127.0.0.1', 
                      user='Elena', 
                      password='1234', 
                      database='PythonReport2_animaldata', 
                      port='1433')
    cur = conn.cursor()
    
    # 擷取資料並存檔
    opts = Options() # 命令行參數
    opts.add_argument('--headless') # 參數設定
    opts.add_argument('--disable-gpu') # 參數設定
    # driver = webdriver.Chrome('chromedriver', chrome_options=opts) # 呼叫selenium開啟Chrome
    # driver = webdriver.Chrome('chromedriver')
    
    url = 'https://asms.coa.gov.tw/Amlapp/App/AnnounceMent.aspx?PageType=Adopt' # 目標網址
    # html_path = driver.get(url) # 呼叫selenium打開目標網址
    # driver.implicitly_wait(10)
    
    # titleCount = int(driver.find_element_by_id('Count_Total').text)  #總隻數
    # driver.close()
    
    # if titleCount % 200 == 0:
    #     TC = int(titleCount / 200)
    # else:
    #     TC = int(titleCount / 200) + 1
    # print(TC)
    
    for i in range(1, 40):
        if i == 20:
            pass
        else:
            print(i)
            currentPage = str(i)
            url = "https://asms.coa.gov.tw/Asms/api/ViewNowAnimal?pageSize=200&currentPage=" + currentPage + "&sortDirection=DESC&sortFields=AcceptDate"
        
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}   
    
            response = requests.get(url = url, headers = headers, verify = False)
            
            content = response.content.decode()
            # content為json格式
            content_list = json.loads(content) #['subjects']
            
            today = datetime.datetime.today()
    
            for item in content_list:
                inmonth = item['AcceptDate']
                inmonth = inmonth[0:7]
                
                indate = item['AcceptDate']
                indate = indate.replace('T00:00:00' , '')
                indate = datetime.datetime.strptime(indate, '%Y-%m-%d')
                indate = today - indate
                indate = str(indate.days)
                indays = indate.replace('T00:00:00' , '')
        
                pic = item['pic']
                if pic == "":
                    pic = 'https://asms.coa.gov.tw/Amlapp/images/defaultSmall.jpg'
                else:
                    pic = 'https://asms.coa.gov.tw/Amlapp/Upload/Pic/' + pic
                    pic = pic.replace('.jpg' , '_org.jpg')
                    pic = pic.replace('.JPG' , '_org.jpg')
                
                sex = item['Sex']
                if sex == 1:
                    sex = "公" 
                elif sex == 2:
                    sex = "母" 
                else:
                    sex = 'x' # 性別不明
                # 收容所代碼
                userTag = ['AAAAG', 'AAACG', 'AAADG', 'AAAEG', 'AAAFG', 'AAAGG',
                            'AAAHG', 'AAAIG', 'AAAJG', 'BAAAG', 'CAAAG', 'DAAAG',
                            'EAAAG', 'FAAAG', 'GAAAG', 'HAAAG', 'IAAAG', 'JAAAG',
                            'LAAAG', 'LAABG', 'MAAAG', 'NAAAG', 'OAAAG', 'PAAAG',
                            'QAAAG', 'RAAAG', 'TAAAG', 'UAAAG', 'UAABG', 'VAAAG',
                            'XAAAG', 'YAAAG']
                # 收容所名稱
                userName = ["新北市政府動物保護防疫處", "新北市新店區公立動物之家",
                            "新北市板橋區公立動物之家", "新北市中和區公立動物之家",
                            "新北市淡水區公立動物之家", "新北市瑞芳區公立動物之家",
                            "新北市五股區公立動物之家", "新北市八里區公立動物之家",
                            "新北市三芝區公立動物之家", "宜蘭縣流浪動物中途之家",
                            "桃園市動物保護教育園區", "新竹縣公立動物收容所",
                            "苗栗縣生態保育教育中心(動物收容所)", "臺中市動物之家南屯園區",
                            "彰化縣流浪狗中途之家", "南投縣公立動物收容所",
                            "雲林縣流浪動物收容所", "嘉義縣流浪犬中途之家",
                            "高雄市壽山動物保護教育園區", "高雄市燕巢動物保護關愛園區",
                            "屏東縣公立犬貓中途之家", "臺東縣動物收容中心",
                            "花蓮縣流浪犬中途之家", "澎湖縣流浪動物收容中心",
                            "基隆市寵物銀行", "新竹市動物保護教育園區",
                            "嘉義市動物保護教育園區", "臺南市動物之家灣裡站",
                            "臺南市動物之家善化站", "臺北市動物之家",
                            "連江縣流浪犬收容中心", "金門縣動物收容中心"]
                # 收容所電話
                userTel = ["02-29596353", "02-22159462", "02-89662158", "02-86685547",
                            "02-26267558", "02-24063481", "02-82925265", "02-26194428",
                            "02-26365436", "039602350 #620", "03-4861760", "03-5519548",
                            "037-558228", "04-23850976", "04-8590638", "049-2225440",
                            "", "05-2950053", "07-5519059", "07-6051002", "0905-981-077",
                            "089-362011", "038-421452", "06-9213559", "02-24560148",
                            "03-5368329", "05-2168661", "06-2964439", "06-5832399",
                            "02-87913254", "0836-25003", "082-336625"]
                # 收容所地址
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
                
                for tag, name, tel, addr in zip(userTag, userName, userTel, userAddr):
                    if item['UserTag'] == tag:
                        asylumnm = name
                        asylumtel = tel
                        asylumaddr = addr
                        
                reasonLt1 = [13, 14, 15, 138, 1275, 1622, 1632]
                reasonLt2 = ["動物救援", "拾獲送交", "不擬續養", "政府捕捉", "依法沒入", "收容所轉入", "其他"]
                for l1, l2 in zip(reasonLt1, reasonLt2):
                    if item["Reason"] == l1:
                        inreason = l2
                    else:
                        inreason = "non"
                    
                res = requests.get(pic)
                pic_name = item['AcceptNum'] + ".jpg"
                picfile_name = '.\\pic\\' + pic_name
                # 將圖片存入指定資料夾
                with open (picfile_name, 'wb') as picfile:
                    picfile.write(res.content)
                
                # 將圖片分貓狗存入指定資料夾，以便後續視覺辨識使用
                # 貓
                if item['TypeId'] == 2:
                    res_cat = requests.get(pic)
                    cat_pic_name = item['AcceptNum'] + ".jpg"
                    cat_picfile_name = '.\\VR_pic\\cat\\' + cat_pic_name
                    with open (cat_picfile_name, 'wb') as picfile:
                        picfile.write(res_cat.content)
                # 狗
                elif item['TypeId'] == 1:
                    res_dog = requests.get(pic)
                    dog_pic_name = item['AcceptNum'] + ".jpg"
                    dog_file_name = '.\\VR_pic\\dog\\' + dog_pic_name
                    with open (dog_file_name, 'wb') as picfile:
                        picfile.write(res_dog.content)
                        
                endDay = today.strftime("%Y/%m/%d")
                                        
                data = {'type' : int(2),
                        'isid' : item['AcceptNum'],
                        'indate' : item['AcceptDate'], # 入所日期
                        "inmonth" : inmonth, # 入所月份
                        'indays' : indays, # 入所天數
                        'title' : item['AcceptNum'], # 收容編號
                        'chip' : item['ChipNum'], # 晶片號碼
                        'inreasoncode' : str(item['Reason']), # 進所原因代碼
                        "inreason" : inreason, # 進所原因
                        'class' : int(item['TypeId']), # 動物別編號(1 = 狗, 2 = 貓)
                        'classname' : item['TypeIdName'], # 動物別(貓、狗...)
                        'variety' : item['BreedName'], # 動物品種
                        'color' : item['CoatName'], # 毛色
                        'area' : item['areaName'], # 來源行政區
                        'sex' : sex, #char(10) 動物性別編號 1 = 公, 2 = 母, x = 性別不明
                        'name' : item['AcceptNum'], # 動物名
                        "endDay" : str(endDay), # 最後能找到該筆資料的那天
                        "userTag" : item['UserTag'], # 公告收容所代號
                        'asylumnm' : asylumnm, #公告收容所名稱
                        'asylumtel' : asylumtel, # 公告收容所電話
                        'asylumaddr' : asylumaddr, #公告收容所地址
                        'note' : item['Note'], # 備註描述
                        'photo' : str(pic), #照片網址
                        'weburl' : 'https://asms.coa.gov.tw/Amlapp/App/AnnounceList.aspx?Id=' + str(item['AnimalId']) + '&AcceptNum=' + item['AcceptNum'] + '&PageType=Adopt', # 頁面網址
                        'piclocalurl' : 'C:\\Users\\miomio-NB\\Desktop\\PythonII_資料擷取(爬蟲)_期末作業_公館\\pic\\' + pic_name,
                        }
                # 如果貓狗還在收容所就修改endDay欄位
                cur.execute("SELECT * FROM animal_load WHERE isid=%s", data['isid'])
                isiddata = cur.fetchall()
                if len(isiddata):
                    target = str(isiddata[0][0])
                    try:
                        sql = "UPDATE animal_load SET endDay='" + data['endDay'] + "' WHERE mainid=" + target
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
                                '''INSERT INTO animal_load(type, isid, indate, 
                                inmonth, indays, title, chip, inreasoncode, 
                                inreason, class, classname, variety, color, 
                                area, sex, name, userTag, asylumnm, asylumtel, 
                                asylumaddr, note, photo, weburl, piclocalurl) 
                                Values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                                %s, %s)''',
                                [(data['type'], data['isid'], data['indate'], 
                                  data['inmonth'], 
                                  data['indays'], data['title'], data['chip'], 
                                  data['inreasoncode'], data["inreason"], 
                                  data['class'], data['classname'], data['variety'], 
                                  data['color'], data['area'], data['sex'], 
                                  data['name'], 
                                  data['userTag'], data['asylumnm'], data['asylumtel'], 
                                  data['asylumaddr'], data['note'], data['photo'], 
                                  data['weburl'], data['piclocalurl'])]
                                        )
                
                        conn.commit()
                        print('新增一筆紀錄')
                    except:
                        conn.rollback()
                        print('新增記錄失敗...')
                        pass
            time.sleep(10)
    
    
    
    data_read = pd.read_sql("SELECT * FROM animal_load", con = conn)
    # data_read = data_read[data_read["indays"] < 10000]
    # 將資料庫內容讀出為CSV檔
    data_read.to_csv(".\\animal_asysulm_heroku\\animal_data_copy.csv", index=False)
    
    cur.close()        
    conn.close()
    print("資料下載完成")

# 定時器
# schedule.every().day.at("00:00").do(animal_download)

# while True:
#     try:
#         schedule.run_pending()
#         time.sleep(1)
#     except:
#         continue
    
animal_download()


    