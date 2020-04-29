#all_cars=[[year,brand,model,price,function,body,city,item_link]]
Number=0
print("how many pages do you want to search? ",end='')
Number=int(input())

import csv
import requests
import re
import bs4
import mysql.connector
config = {'user': 'root','password': 'password','host': '127.0.0.1' }    
createDatabase="CREATE DATABASE bamaCars CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
sql= "INSERT INTO all_cars VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
createTable="CREATE TABLE all_cars (year VARCHAR(255),brand VARCHAR(255),model VARCHAR(255),price_Toman VARCHAR(255),karkard_Km VARCHAR(255),body VARCHAR(255),city VARCHAR(255),item_link VARCHAR(255))"        
karkard='كاركرد'; badane='بدنه'; ostan='شهرستان';
year,brand,model,price,function,body,city,rep='','','','','','','',0
print("Searching Started"); print("Number of scaned pages is: ",end='');

agree=0



cnx=mysql.connector.connect(**config)
cursor=cnx.cursor()
mycursor=cnx.cursor()
try:
    cursor.execute(createDatabase)
except:
    pass
cursor.execute("USE bamaCars")
try:
    cursor.execute(createTable)
except:
    pass

for page in range(1,Number+1):
    print(page,end=" ")
    url=requests.get("https://bama.ir/car/all-brands/all-models/all-trims?body=passenger-car&instalment=0&sort=2&page=%d" %page)
    soup=bs4.BeautifulSoup(url.text,'html.parser')
    links=soup.find_all('a',attrs={'itemprop':'url', 'class':"cartitle cartitle-desktop"})
    for i in range(12):
        rep=0
        cursor.execute("SELECT item_link FROM all_cars")
        myresult=cursor.fetchall()
        item_link=links[i].attrs.get("href")
        for row in myresult:
            q12=str(row)
            q12=(q12.strip("()',"))
            if(q12==item_link):
                rep=1
                break         
        if(rep==1):
            continue           
        itemurl=requests.get(links[i].attrs.get("href"))
        itemsoup=bs4.BeautifulSoup(itemurl.text,'html.parser')
        price=itemsoup.find('span',attrs={'itemprop':'price'}).text.strip()          
        if(price=='توافقی'):
            agree+=1
            continue
        price=re.sub(r',','',price).strip()
        if(price=='در توضیحات'):
            x=itemsoup.find('span',attrs={'style':'font-weight:bold; padding-right: 25px'}).text.strip()
            x=re.sub(r'قیمت پیشنهادی فروشنده:','',x)
            price=re.sub(r'تومان','',x).strip()
            price=re.sub(r',','',price).strip()
        year=itemsoup.find('span',attrs={'itemprop':"releaseDate"}).text.strip()
        brand=itemsoup.find('span',attrs={'itemprop':"brand"}).text.strip()
        model=itemsoup.find('span',attrs={'itemprop':"model"}).text.strip()
        anyobj=itemsoup.find_all('p')
        for row in anyobj:
            q=row.text.strip()
            if(karkard in q):        
                function=re.sub(r'كاركرد','',q).strip()
                function=re.sub(r'کیلومتر','',function).strip()
                function=re.sub(r',','',function).strip()
            if(badane in q):
                body=re.sub(r'بدنه','',q).strip()
            if(ostan in q):
                city=re.sub(r'شهرستان','',q).strip()
        val=(year,brand,model,price,function,body,city,item_link)
        cursor.execute(sql ,val)
        cnx.commit()
        
        
        
    
cursor.execute("SELECT * FROM all_Cars")
myresult=cursor.fetchall()   
    



with open('carData.csv', mode='w',encoding='utf-8-sig',newline='') as car_Data:
    car_writer = csv.writer(car_Data, delimiter=',')
    car_writer.writerow(['brand','model','year','karkard','body','price(MillionToman)','city','link'])
    for row in myresult:
        try:
            x=int(row[3])
            x=x/1000000
            x=str(x)
            car_writer.writerow([row[1],row[2],row[0],row[4],row[5],x,row[6],row[7]])
        except:
            car_writer.writerow([row[1],row[2],row[0],row[4],row[5],row[3],row[6],row[7]])
    


cnx.commit()
cursor.close()
cnx.close()
print("\nnot accepted is:",agree,"\nDone!!")






