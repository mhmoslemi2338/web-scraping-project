
import csv
import mysql.connector
config = {'user': 'root','password': 'password','host': '127.0.0.1' }    

hpr=0
city=''
hkr=0
yr=0
q1234=''
wer=''
print(" enter yor car options below")

while(True):
    print('maximum price(each unit is one million toman): ',end='')
    wer=input()
    hpr=wer
    if(wer!='?'):
        hpr=int(hpr)
    print('maximum karkard(in Km): ',end='')
    wer=input()
    hkr=wer
    if(wer!='?'):
        hkr=int(hkr)
    print('which city(type in persian): ',end='')
    city=input()
    print('after which year: ',end='')
    wer=input()
    yr=wer
    if(wer!='?'):
        yr=int(yr)
    
    
    print("do you want to change options?(y,n) ",end='')
    q1234=input()
    if(q1234=='n'):
        break


cnx=mysql.connector.connect(**config)
cursor=cnx.cursor()
cursor.execute("USE bamaCars")
cursor.execute("SELECT * FROM all_Cars")
myresult=cursor.fetchall()



with open('yourCars.csv', mode='w',encoding='utf-8-sig',newline='') as car_Data:
    car_writer = csv.writer(car_Data, delimiter=',')
    car_writer.writerow(['brand','model','year','karkard(Km)','body','price(MillionToman)','city','link'])
    for row in myresult:
        try:
            city1=row[6]
            x=int(row[3])
            x=x/1000000
            if( x<=hpr and city1==city  and int(row[0])>=yr  and int(row[4])<=hkr ):
                x=str(x)
                car_writer.writerow([row[1],row[2],row[0],row[4],row[5],x,row[6],row[7]])
        except:
            pass
            #car_writer.writerow([row[1],row[2],row[0],row[4],row[5],row[3],row[6],row[7]])
            
    
    


cnx.commit()
cursor.close()
cnx.close()
print('yourcars.csv is ready')

